from flask import request

def hasvoted(vote_id):
    if not request.cookies.get("vt"):
        return False

    cookies = map(int, request.cookies.get("vt").split("."))
    print()
    print(cookies)
    print()
    if vote_id in cookies:
        return True
    
    return False
