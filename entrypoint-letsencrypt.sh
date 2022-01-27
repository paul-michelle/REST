#!/bin/bash

if ! [ -x "$(command -v docker-compose)" ]; then
  echo 'Error: docker-compose is not installed.' >&2
  exit 1
fi

domains=(tickets.paul-michelle.art www.tickets.paul-michelle.art)
data_path="./data/certbot"
email="lieber.paul.git@gmail.com"

staging=0
rsa_key_size=4096

domains_str=${domains[*]}
domains_comma_sep=${domains_str//${IFS:0:1}/, }

if [ -d "$data_path" ]; then
  read -r -p "Already existing data found for $domains_comma_sep. Replace certificate? (y/N) " decision
  if [ "$decision" != "Y" ] && [ "$decision" != "y" ]; then
    exit
  fi
fi

if [ ! -e "$data_path/conf/options-ssl-nginx.conf" ] || [ ! -e "$data_path/conf/ssl-dhparams.pem" ]; then
  echo "### Downloading recommended transport layer security parameters ..."
  mkdir -p "$data_path/conf"
  curl -s https://raw.githubusercontent.com/certbot/certbot/master/certbot-nginx/certbot_nginx/_internal/tls_configs/options-ssl-nginx.conf >"$data_path/conf/options-ssl-nginx.conf"
  curl -s https://raw.githubusercontent.com/certbot/certbot/master/certbot/certbot/ssl-dhparams.pem >"$data_path/conf/ssl-dhparams.pem"
  echo
fi

echo "### Launching docker-compose with a certbot image to create a DUMMY certificate for $domains_comma_sep ..."
path="/etc/letsencrypt/live/${domains[0]}"
mkdir -p "$data_path/conf/live/${domains[0]}"

docker-compose run --rm --entrypoint "\
  openssl req -x509 -nodes -newkey rsa:1024 -days 1\
    -keyout '$path/privkey.pem' \
    -out '$path/fullchain.pem' \
    -subj '/CN=localhost'" certbot

echo "### Forcing to recreate nginx-container ..."
docker-compose up --force-recreate -d nginx

echo "### Deleting the dummy certificate for $domains_comma_sep ..."
docker-compose run --rm --entrypoint "\
  rm -Rf /etc/letsencrypt/live/${domains[0]} && \
  rm -Rf /etc/letsencrypt/archive/${domains[0]} && \
  rm -Rf /etc/letsencrypt/renewal/${domains[0]}.conf" certbot

echo "### With challenge stage passed, moving to Production Let's Encrypt Certificate request stage for $domains_comma_sep ..."
echo "### Setting domains flag argument ..."
domain_args=""
for domain in "${domains[@]}"; do
  domain_args="$domain_args -d $domain"
done

echo "### Setting email flag argument ..."
case "$email" in
"") email_arg="--register-unsafely-without-email" ;;
*) email_arg="--email $email" ;;
esac

echo "### Setting staging flag argument ..."
if [ $staging != "0" ]; then staging_arg="--staging"; fi

echo "### With all arguments set, launching docker-compose with a certbot image in a \"certonly\" mode\
 to create a PRODUCTION certificate for $domains_comma_sep ..."
docker-compose run --rm --entrypoint "\
  certbot certonly --webroot -w /var/www/certbot \
    $staging_arg \
    $email_arg \
    $domain_args \
    --rsa-key-size $rsa_key_size \
    --agree-tos \
    --force-renewal" certbot

echo "### With Production Let's Encrypt Certificate received, executing nginx-container reload ..."
docker-compose exec nginx nginx -s reload
echo "### Easy-peasy-lemon-squeezy ..."
