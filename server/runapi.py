from flask import Flask,request,jsonify
import json, requests, hashlib, random
from urllib import quote

app = Flask(__name__)

def encrypted_id(id):
	magic = bytearray('3go8&$8*3*3h0k(2)2')
	song_id = bytearray(id)
	magic_len = len(magic)
	for i in xrange(len(song_id)):
		song_id[i] = song_id[i] ^ magic[i % magic_len]
	m = hashlib.md5(song_id)
	result = m.digest().encode('base64')[:-1]
	result = result.replace('/', '_')
	result = result.replace('+', '-')
	return result

@app.route("/eapi/song/enhance/<player_or_download>/url", methods=['GET','POST'])
def get_song_api(player_or_download):
	if (not 'ids' in request.args):
		return get_ios_response(player_or_download)
	origin_result = requests.post('http://music.163.com/eapi/song/enhance/' + player_or_download + '/url?br=' + quote(request.args['br']) + '&ids=' + quote(request.args['ids']), data={'params':request.form['params']}, headers={'Cookie':request.headers['Cookie']})
	origin_result_json = json.loads(origin_result.content)
	if (player_or_download == 'player' and origin_result_json['data'][0]['url'] != None):
		print('Returning original player result')
		return origin_result.text
	if (player_or_download == 'download' and origin_result_json['data']['url'] != None):
		print('Returning original download result')
		return origin_result.text
	song_id = json.loads(request.args['ids'])[0]
	song_id = song_id[0:song_id.find('_')]
	return jsonify(get_music_resource(song_id, player_or_download))

def get_ios_response(player_or_download):
	origin_result = requests.post('http://music.163.com/eapi/song/enhance/' + player_or_download + '/url', data={'params':request.form['params']})
	origin_result_json = json.loads(origin_result.content)
	if (player_or_download == 'player' and origin_result_json['data'][0]['url'] != None):
		print('Returning original player result')
		return origin_result.text
	if (player_or_download == 'download' and origin_result_json['data']['url'] != None):
		print('Returning original download result')
		return origin_result.text
	if (player_or_download == 'player'):
		song_id = str(origin_result_json['data'][0]['id'])
	else:
		song_id = str(origin_result_json['data']['id'])
	return jsonify(get_music_resource(song_id, player_or_download))

def get_music_resource(song_id, player_or_download):
	request_result = requests.get('http://music.163.com/api/song/detail/?ids=' + quote('["' + song_id + '"]') + '&id=' + song_id)
	result_json = request_result.json()
	song_res = result_json['songs'][0]['hMusic'] or result_json['songs'][0]['bMusic'] or result_json['songs'][0]['audition']

	song_res_id = str(song_res['dfsId'])
	file_ext = song_res['extension']
	file_size = song_res['size']
	song_br = song_res['bitrate']
	
	mp3_url = "http://m%s.music.126.net/%s/%s.%s" % (random.randrange(1, 3), encrypted_id(song_res_id), song_res_id, file_ext)
	if (player_or_download == 'player'):
		print('Returning new player result')
		return {
			'code' : 200,
			'data' : [
				{
					'id' : int(song_id),
					'url': mp3_url,
					'br' : song_br,
					'size': file_size,
					'md5' : None,
					'code': 200,
					'expi': 1200,
					'type': file_ext,
					'gain': 0,
					'fee': 0,
					'canExtend':False
				}
			]
		}
	else:
		print('Returning new download result')
		return {
			'code' : 200,
			'data' : {
				'id' : int(song_id),
				'url': mp3_url,
				'br' : song_br,
				'size': file_size,
				'md5' : None,
				'code': 200,
				'expi': 1200,
				'type': file_ext,
				'gain': 0,
				'fee': 0,
				'canExtend':False,
				'uf': None,
				'payed': 0
			}
		}

if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0', port=5001)
