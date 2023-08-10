# production only
from waitress import serve
from phonemic import create_app 

serve(create_app(), host='0.0.0.0', port=8091)