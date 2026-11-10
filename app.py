import json,os,uuid
from urllib.parse import urlparse,parse_qs
from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
R=os.path.dirname(__file__);D=R+'/data.json'
def load():
 if not os.path.exists(D): save({'documents':[],'shares':[],'comments':[],'versions':[],'users':['ivan','grace']})
 return json.load(open(D))
def save(x): json.dump(x,open(D,'w'),indent=2)
class H(BaseHTTPRequestHandler):
 def j(self,x,c=200):
  b=json.dumps(x).encode();self.send_response(c);self.send_header('Content-Type','application/json; charset=utf-8');self.end_headers();self.wfile.write(b)
 def do_GET(self):
  d=load()
  if urlparse(self.path).path=='/api/presence':
   now=__import__('time').time();return self.j({'online':[u for u,t in d.get('presence',{}).items() if now-t<30]})
  if urlparse(self.path).path=='/api/versions': return self.j([v for v in d.get('versions',[]) if v['document']==parse_qs(urlparse(self.path).query).get('document',[''])[0]])
  if urlparse(self.path).path=='/api/comments': return self.j([v for v in d.get('comments',[]) if v['document']==parse_qs(urlparse(self.path).query).get('document',[''])[0]])
  if urlparse(self.path).path=='/api/documents':
   user=parse_qs(urlparse(self.path).query).get('user',['ivan'])[0]
   docs=[]
   for x in d['documents']:
    owned=x['owner']==user; shared=any(z['document']==x['id'] and z['user']==user for z in d['shares'])
    if owned or shared: docs.append(dict(x,access='Owned' if owned else 'Shared'))
   return self.j({'documents':docs,'users':d['users'],'shares':d['shares']})
  self.send_response(200);self.send_header('Content-Type','text/html; charset=utf-8');self.end_headers();self.wfile.write(open(R+'/static/index.html','rb').read())
 def do_POST(self):
  q=json.loads(self.rfile.read(int(self.headers.get('Content-Length',0))) or b'{}');d=load()
  if self.path=='/api/presence':
   d.setdefault('presence',{})[q.get('user','ivan')]=__import__('time').time();save(d);return self.j({'ok':True})
  if self.path=='/api/comments':
   d.setdefault('comments',[]).append({'id':uuid.uuid4().hex[:8],'document':q.get('document'),'user':q.get('user','ivan'),'text':q.get('text','')});save(d);return self.j({'ok':True})
  if self.path=='/api/share':
   if q.get('user') not in d['users']: return self.j({'error':'Unknown user'},400)
   item={'document':q.get('document'),'user':q['user'],'role':q.get('role','viewer')}
   if item not in d['shares']: d['shares'].append(item);save(d)
   return self.j({'ok':True,'share':item})
  x={'id':uuid.uuid4().hex[:8],'title':q.get('title','Untitled document'),'content':q.get('content','<p></p>'),'owner':'ivan'};d['documents'].append(x);save(d);self.j(x,201)
 def do_PUT(self):
  q=json.loads(self.rfile.read(int(self.headers.get('Content-Length',0))));d=load();x=next(x for x in d['documents'] if x['id']==self.path.split('/')[-1]);user=self.headers.get('X-User','ivan');share=next((z for z in d.get('shares',[]) if z['document']==x['id'] and z['user']==user),None)
  if x['owner']!=user and (not share or share.get('role')!='editor'): return self.j({'error':'Read-only document'},403)
  d.setdefault('versions',[]).append({'document':x['id'],'title':x.get('title'),'content':x.get('content'),'timestamp':__import__('datetime').datetime.now().isoformat()});x.update(q);save(d);self.j(x)
os.makedirs(R+'/static',exist_ok=True);ThreadingHTTPServer(('127.0.0.1',8000),H).serve_forever()
