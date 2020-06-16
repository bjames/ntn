import requests


def curl(url):

    try:
        response = requests.head(url)
        print(response)
        return response.headers, response.status_code, response.elapsed.total_seconds()

    except requests.exceptions.MissingSchema:
        return curl('https://' + url)

    except requests.exceptions.SSLError:
        return {'Error': 'Invalid SSL Certificate'}, None, None

    except requests.exceptions.InvalidURL:
        return {'Error': 'Check provided hostname, valid input includes IP addresses and hostnames'}, None, None

    except requests.exceptions.InvalidSchema:
        return {'Error': 'Invalid protocol, valid protocols include HTTP and HTTPS'}, None, None

    except requests.exceptions.ConnectionError as e:

        error_str = str(e)

        if 'timed' in error_str:
            return {'Error': 'Connection timed out'}, None, None
        elif 'refused' in error_str:
            return {'Error': 'Connection refused'}, None, None
        elif 'Name or service' in error_str:
            return {'Error': 'DNS resolution failed or an invalid hostname was provided'}, None, None
        elif 'Invalid' in error_str:
            return {'Error': 'Check provided hostname, valid input includes IP addresses and hostnames'}, None, None
        else:
            return {'Error': error_str}, None, None


if __name__ == '__main__':

    print(curl('https://neverthenetwork.com'))
    print(curl('https://beta.neverthenetwork.com'))
    print(curl('0.0.0.1'))
    print(curl('http://neverthenetwork.com/thisisatest'))
    print(curl('192.168.1.1'))