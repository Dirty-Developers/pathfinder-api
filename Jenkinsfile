node() {
    def image = null
    stage('Checkout') {
        checkout scm
    }

    stage('Build') {
        image = docker.build("pathfinder-api:${env.BUILD_ID}")
    }

    stage('Deploy'){
        try{
            sh 'docker stop pathfinder-api && docker rm pathfinder-api'
        }catch(Exception e){
            echo e.getMessage()
        }

        withCredentials([string(credentialsId: 'HOTELAPI_KEY', variable: 'hotel_key')]) {
            withCredentials([string(credentialsId: 'HOTELAPI_SECRET', variable: 'hotel_secret')]) {
                withCredentials([string(credentialsId: 'ACTAPI_KEY', variable: 'act_key')]) {
                    withCredentials([string(credentialsId: 'ACTAPI_SECRET', variable: 'act_secret')]) {
                        withCredentials([string(credentialsId: 'YELP_API_ID', variable: 'yelp_id')]) {
                            withCredentials([string(credentialsId: 'YELP_API_KEY', variable: 'yelp_key')]) {
                                def runArgs = '\
-e "HOTELAPI_KEY=$hotel_key" \
-e "HOTELAPI_SECRET=$hotel_secret" \
-e "ACTAPI_KEY=$act_key" \
-e "ACTAPI_SECRET=$act_secret" \
-e "YELP_ID=$yelp_id" \
-e "YELP_KEY=$yelp_key" \
-e "DB_PATH=/usr/local/pathfinder/pathfinder.db" \
-p 80:5000 \
--name pathfinder-api'

                                 def container = image.run(runArgs)
                            }
                        }
                    }
                }
            }
        }
    }
}

