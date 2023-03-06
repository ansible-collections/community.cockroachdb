[![COLLECTION_NAME](URL/workflows/Plugins%20CI/badge.svg?event=push)]


cd ~/ansible-build-date
git checkout main
git pull upstream main
cd <~/DASHBOARD-REPO-DIR>
grep repository ~/ansible-build-data/7/collection-meta.yaml | cut -f 2-20 -d ':' |tr -d ' ' > urls.txt
