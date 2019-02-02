# AppleMusic Elastic

## Description
  This project purpose is to import AppleMusic logged activity into Elasticsearch.

  [Check the demo here](http://bit.ly/2WBvi2O)

## Getting the AppleMusic datas

  Ask Apple for your AppleMusic GDPR datas [here](https://privacy.apple.com/)
  * Log you in
  * Choose `Get a copy of your data`
  ![Ask for datas](https://blog.cypressxt.net/wp-content/uploads/2018/10/AskAppleData.png)
  * Select `App Store, Itunes Store, Ibook Store AppleMusic activity` in the Apple GDPR downloadable data sets
  ![AppleMusic](https://blog.cypressxt.net/wp-content/uploads/2018/10/SelectDatas.png)
  * Choose the `maximum file size`
  ![Max file size](https://blog.cypressxt.net/wp-content/uploads/2018/10/ChooseFileSize.png)
  * Wait until Apple finished the extract preparation (usually took ~ 7 days)
  ![Wait](https://blog.cypressxt.net/wp-content/uploads/2018/10/WaitAvailable.png)
  * Download the Zip file
  ![Download](https://blog.cypressxt.net/wp-content/uploads/2018/10/DownloadData.png)

## Useful file
  You can find the useful file in the downloaded Zip file under `App Store, iTunes Store, iBooks Store, Apple Music/App_Store_iTunes_Store_iBooks_Store_Apple_Music/Apple Music Activity/Apple Music Play Activity.csv`

## Script usage
  Get the Python script [applemusic_to_es.py](applemusic_to_es.py)

### Setup
  Before injecting the AppleMusic data into Elasticsearch, you need to setup the index template and create the kibana visualizations.

  You can do it so by using the `setup` command:
  ```
./applemusic_to_es.py setup -e http://es-server:9200 -k http://kibana-server:5601
Elasticsearch & kibana Setup...
 Elasticsearch http://es-server:9200
 Kibana http://kibana-server:5601
     template downloaded from Github
         template applied
     visualizations downloaded from Github
         pushing dashboard [AppleMusic] Overview
         pushing index-pattern applemusic-*
         pushing visualization [AppleMusic] Skipped pie
         pushing visualization [AppleMusic] Single songs played
         pushing visualization [AppleMusic] Feature pie
         pushing visualization [AppleMusic] Song listened over time
         pushing visualization [AppleMusic] Top 10 songs
         pushing visualization [AppleMusic] Top 10 artists
         pushing visualization [AppleMusic] Listened hours
         pushing visualization [AppleMusic] Avg song played / day
         pushing visualization [AppleMusic] avg listening hours / day
  ```
  If your elasticsearch or kibana endpoint is using HTTP basic auth, use the `-x username` option. You will be resqueted to type your basic auth password.
  ```
  ./applemusic_to_es.py setup -e http://es-server:9200 -k http://kibana-server:5601 -x username
  ```

### Inflate

  Once you've the `Apple Music Play Activity.csv` file, use the `applemusic_to_es.py` script like this to fill the `applemusic-*` index:
  ```
  ./applemusic_to_es.py inflate -i /myfolder/Apple\ Music\ Play\ Activity\ 29-01-2018.csv -e http://es-server:9200
  Reading CSV file...
  Generating json bulk datas...
  Elasticsearch insertion...
  		insertion 5000/109042 events...
  		insertion 10000/109042 events...
  		insertion 15000/109042 events...
  		[...]
  		insertion 100000/109042 events...
  		insertion 105000/109042 events...
  		insertion 109043/109042 events...
  ```
  If your elasticsearch endpoint is using HTTP basic auth, use the `-x username` option. You will be resqueted to type your basic auth password.
  ```
  ./applemusic_to_es.py inflate -i /myfolder/Apple\ Music\ Play\ Activity\ 29-01-2018.csv -e http://es-server:9200 -x username
  ```

## Elasticsearch
  After the `applemusic_to_es.py` script excecution you will be able to browse your AppleMusic play activity in Kibana. Should look like this:
  ![AppleMusic Kibana](https://blog.cypressxt.net/wp-content/uploads/2018/10/AppleMusicKibana.jpg)

### Visualizations
  Visualizations are created during the [`setup`](#setup).
  ![AppleMusic Visualization](https://blog.cypressxt.net/wp-content/uploads/2018/10/song_over_time.png)
### Dashboards
  The dashboard is created during the [`setup`](#setup).
  ![AppleMusic Dashboard](https://blog.cypressxt.net/wp-content/uploads/2018/10/appleMusic_dashboard.png)
