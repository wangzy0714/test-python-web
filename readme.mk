请求上下文 request ， session
request封装客户端发送请求的报文数据，请求体 url 参数 请求头 

session，存储数据，基于cookie，存在客户端 使用时需要增加密钥,每次获取session都需要设置cookie，如果浏览器拒绝cookie，session就无法使用
app.config['SECRET_KEY'] = '123456'

key value的形式进行使用
session['key'] = 'value'

默认的生命周期就是浏览器关闭即消失
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(seconds=60*5)
