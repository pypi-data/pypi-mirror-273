import requests 
def Info_Insta(user_name):
	url = f"https://www.instagram.com/api/v1/users/web_profile_info/?username={user_name}"
	headers = {
	    "X-Ig-App-Id": "1217981644879628",
	}
	try:
	    req = requests.get(url ,headers=headers).json()
	    bio = req["data"]["user"]["biography"]
	    followers = req["data"]["user"]["edge_followed_by"]["count"]
	    following = req["data"]["user"]["edge_follow"]["count"]
	    fullname = req["data"]["user"]["full_name"]
	    idd =  req["data"]["user"]["id"]
	    username = req["data"]["user"]["username"]
	    z=requests.get(f'https://o7aa.pythonanywhere.com/?id={idd}').json()
	    date=z['date']
	    infoo = f"""
    \r     ( ACCOUNT INSTAGRAM )
    
	USERNAME : {username}
	FULL NAME : {fullname}
	FOLLOWERS : {followers}
	FOLLOWING : {following}
	BIO : {bio}
	ID : {idd}
	DATE : {date}
	programmer : ibrahim : telegram @B_xxBx"""
	    return infoo
	except Exception as e:
		return e
	