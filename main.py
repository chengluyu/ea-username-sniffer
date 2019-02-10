import requests
import time


URL = 'https://signin.ea.com/p/ajax/user/checkOriginId?requestorid=portal&originId='


def get_candidates():
    f = open('english-words/words_alpha.txt')
    candidates = []
    for w in f:
        if w[-1] == '\n':
            w = w[:-1]
        if len(w) == 4:
            candidates.append(w)
    f.close()
    return candidates


def main():
    failed = open('failed.txt', 'w+')
    available = open('available.txt', 'w+')
    occupied = open('occupied.txt', 'w+')
    candidates = get_candidates()
    print('Get {} candidate(s)'.format(len(candidates)))
    for w in candidates:
        print('Test "{}"...'.format(w))
        try:
            r = requests.get(URL + w)
            obj = r.json()
            if obj['message'] is None:
                print('Available')
                available.write(w + '\n')
            elif obj['message'] == 'origin_id_duplicated':
                print('Occupied')
                occupied.write(w + '\n')
            else:
                message = str(obj['message'])
                print('Failed because of {}'.format(message))
                failed.write('{},{}\n'.format(w, message))
        except KeyboardInterrupt:
            raise
        except:
            print('Failed')
            failed.write(w + '\n')
        time.sleep(0.5)


if __name__ == "__main__":
    main()