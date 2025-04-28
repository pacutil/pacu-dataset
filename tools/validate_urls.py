from urllib.parse import urlparse
import sys

def valid(url):
    try:
        result = urlparse(url)
        
        if result.scheme == 'http' or result.scheme == 'https':
            return all([result.scheme, result.netloc])

        return False

    except Exception:
        return False

def main():
    vf = sys.argv[1] + '.valid'

    with open(vf, 'w') as vfile:
        with open(sys.argv[1], 'r') as file:
            for url in file:
                if valid(url):
                    vfile.write(url)

if __name__ == "__main__":
    main()
