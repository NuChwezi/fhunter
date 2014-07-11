import json
import web
import subprocess
import re

urls = (
  '', 'fhunter',
  '/', 'fhunter',
  '/fortune', 'fortune',
)

#------------- STATIC --------------
BASE_URI = '/fhunter'
APP_TITLE = 'FORTUNE HUNTER'

#------------- DB -------------
db = web.database(dbn='postgres', user='postgres', pw='postgres', db='fhunter', host='localhost')

def record_hit(hit):
    new_id = db.insert('fhunter_hits',seqname='fhunter_hits_id_seq',
            ip = hit['ip'],
            score = hit['score'],
            extra = hit['extra'],
            method = hit['method'] )
    return new_id

#--------- Templates ----------
render = web.template.render('/var/opt/fhunter/templates/', cache=False)

#------ utils------
def get_fortune():
    return subprocess.Popen(['fortune'], stdout=subprocess.PIPE).communicate()[0]

#~~~~~~~~~~~~~~ VIEWS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
SCORE_INCREMENT = 10
PASS_PENALTY = 5

class fhunter:
    def POST(self):
        params = web.input(score=0)
        hit = {
                'ip': web.ctx.ip,
                'score' : params.score,
                'method' : 'POST',
                'extra' : json.dumps( web.ctx.environ.get('HTTP_REFERER','') )
                }
        record_hit( hit )
        fortune = re.split('\s+',get_fortune())
        return render.fhunter({
            'APP_TITLE' : APP_TITLE,
            'BASE_URI' : BASE_URI,
            'fortune' : ' '.join( fortune ).strip(),
            'score' : params.score or 0,
            'SCORE_INCREMENT' : SCORE_INCREMENT * (( len(fortune) / 10 ) or 1),
            'PASS_PENALTY' : PASS_PENALTY * (( len(fortune) / 10 ) or 1),
            'continue' : True
            })
    def GET(self):
        web.ctx.status = '200 OK'
        web.header('Content-Type', 'text/html')
        hit = {
                'ip': web.ctx.ip,
                'score' : None,
                'method' : 'GET',
                'extra' : json.dumps( web.ctx.environ.get('HTTP_REFERER','') )
                }
        record_hit( hit )
        fortune = re.split('\s+',get_fortune())
        return render.fhunter({
            'APP_TITLE' : APP_TITLE,
            'BASE_URI' : BASE_URI,
            'fortune' : ' '.join( fortune ).strip(),
            'score' : 0,
            'SCORE_INCREMENT' : SCORE_INCREMENT * (( len(fortune) / 10 ) or 1),
            'PASS_PENALTY' : PASS_PENALTY * (( len(fortune) / 10 ) or 1),
            'continue' : False
            })


application = web.application(urls, globals()).wsgifunc()

web.webapi.internalerror = web.debugerror
if __name__ == '__main__': application.run()
