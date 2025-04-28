const fs = require('node:fs');
const path = require('path');
const request = require('request');
const readline = require('readline');
const { execSync } = require('child_process');

const phishingExt = '.phishing';
const unlabeledExt = '.unlabeled';

const phishingDirName = 'phishing';
const unlabeledDirName = 'unlabeled';

const minutes = 60 * 1000; // ms
const hours = 60 * minutes; // ms

function Sleep(ms) {
    return new Promise((resolve) => {
        setTimeout(resolve, ms);
    });
}

function CalculateBackOff(n) {
    const rand = Math.random();
    return Math.min(((Math.pow(2, (n - 1)) * 15 * minutes) * (rand + 1)), (24 * hours));
}

function CountLines(filePath) {
    const output = execSync(`wc -l < "${filePath}"`).toString().trim();
    return parseInt(output, 10);
}

async function* StreamURLBatches(filePath, batchSize = 500) {
    const fileStream = fs.createReadStream(filePath, { encoding: 'ascii' });
    const rl = readline.createInterface({ input: fileStream, crlfDelay: Infinity });

    let batch = [];

    for await (const line of rl) {
        const url = line.trim();
        if (url) batch.push(url);

        if (batch.length === batchSize) {
            yield batch;
            batch = [];
        }
    }

    if (batch.length) {
        yield batch;
    }
}

function SendThreatMatchesRequest(server, urls) {
    const route = `http://${server.netloc}/v4/threatMatches:find?key=${server.key}`;
    const threatEntries = urls.map(x => ({ url: x }));
    const body = {
        threatInfo: {
            platformTypes: ['ANY_PLATFORM'],
            threatEntryTypes: ['URL'],
            threatEntries: threatEntries
        }
    };

    return new Promise((resolve, reject) => {
        request({
            headers: {'Content-Type': 'application/json'},
            uri: route,
            body: JSON.stringify(body),
            method: 'POST'
        }, (err, res, body) => {
            if (err) {
                reject(err);
                return;
            }
            if (res.statusCode != 200) {
                reject(`Error ${res.statusCode}`);
                return;
            }
            resolve(body);
        });
    });
}

async function FilterURLs(server, urls) {
    var response;

    try {
        response = await SendThreatMatchesRequest(server, urls);
    } catch (err) {
        throw new Error('SendThreatMatchesRequest() failed', { cause: err });
    }

    try {
        response = JSON.parse(response);
    } catch (err) {
        throw new Error('Failed to parse response', { cause: err });
    }

    const phishing = (() => {
        if (Array.isArray(response.matches)) {
            const urls = response.matches.map(x => x.threat.url);
            return Array.from(new Set(urls));
        }
        return [];
    })();
    const unlabeled = urls.filter(x => !phishing.includes(x));

    return ({ phishing: phishing, unlabeled: unlabeled });
}

async function FilterFile(server, inputFile, outDir) {
    const basename = path.basename(inputFile);
    const phishingFile = path.join(outDir, phishingDirName, `${basename}${phishingExt}`);
    const unlabeledFile = path.join(outDir, unlabeledDirName, `${basename}${unlabeledExt}`);

    [path.dirname(phishingFile), path.dirname(unlabeledFile)].forEach(x => {
        if (!fs.existsSync(x)) {
            fs.mkdirSync(x, { recursive: true });
        }
    });

    let n = 1;
    let processed = 0;
    const total = CountLines(inputFile);

    const batchGen = StreamURLBatches(inputFile, 500);
    let current = await batchGen.next();

    while (!current.done) {
        const urls = current.value;
        const start = Date.now();
        let filtered;

        try {
            filtered = await FilterURLs(server, urls);
        } catch (err) {
            const timeout = CalculateBackOff(n++);
            console.error(`[${inputFile}] Backing off (${(timeout / minutes).toFixed(2)} minutes) !!!\nFilterFile(): FilterURLs(): `, err);
            await Sleep(timeout);
            continue;
        }

        try {
            const writes = [];

            if (filtered.phishing.length > 0) {
                writes.push(fs.promises.appendFile(phishingFile, filtered.phishing.join('\n') + '\n'));
            }

            if (filtered.unlabeled.length > 0) {
                writes.push(fs.promises.appendFile(unlabeledFile, filtered.unlabeled.join('\n') + '\n'));
            }

            if (writes.length > 0) {
                await Promise.all(writes);
            }
        } catch (err) {
            console.error(`[${inputFile}] FilterFile(): fs.promises.appendFile(): `, err);
            continue;
        }

        processed += filtered.phishing.length + filtered.unlabeled.length;
        n = 1;

        const elapsed = Date.now() - start;
        console.log(`[${inputFile}]\t${processed}\t/\t${total}\t(${((processed * 100) / total).toFixed(2)}%)\t${elapsed}ms`);

        current = await batchGen.next();
    }
}

async function main() {
    if (process.argv.length != 4) {
        console.log('Usage: node filter.js <path/to/servers.json> <path/to/tasks.json>');
        process.exit(1);
    }

    const readJSON = (filePath) => {
        const data = fs.readFileSync(filePath, { encoding: 'ascii', flag: 'r' });
        return JSON.parse(data);
    };

    const servers = readJSON(process.argv[2]);
    const tasks = readJSON(process.argv[3]);

    await Promise.all(
        tasks.map((task, index) =>
            FilterFile(servers[index], task.file, task.outdir)
        )
    );
}

main();
