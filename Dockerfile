# Pass BRIEFING_URL, SURGE_LOGIN, SURGE_TOKEN and SURGE_DOMAIN environmental variables when running
FROM node:14-stretch-slim
# install surge.sh CLI as root
RUN npm -g install surge
# switch to regular user
USER node
# pass internal environmental variables
ENV OUTPUT_XML './public/briefing.xml'
ENV APP_PATH '/app'
# copy script from host
COPY --chown=node:node . $APP_PATH
# run script
WORKDIR $APP_PATH
CMD bash ./deploy-to-surge.sh