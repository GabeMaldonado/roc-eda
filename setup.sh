mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"egmaldonado10@gmail.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
enableCORS=false
headless = true\n\
port = $PORT\n\
" > ~/.streamlit/config.toml