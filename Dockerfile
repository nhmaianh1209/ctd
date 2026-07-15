FROM nginx:1.27-alpine

# Install envsubst for runtime config injection
RUN apk add --no-cache gettext

COPY nginx.conf /etc/nginx/templates/default.conf.template

# Static files
COPY . /usr/share/nginx/html

# Remove server-side files from static root
RUN rm -f /usr/share/nginx/html/nginx.conf \
           /usr/share/nginx/html/docker-compose.yml \
           /usr/share/nginx/html/.env

EXPOSE 80
CMD ["sh", "-c", "envsubst '$MSAL_CLIENT_ID $MSAL_TENANT_ID' < /etc/nginx/templates/default.conf.template > /etc/nginx/conf.d/default.conf && nginx -g 'daemon off;'"]
