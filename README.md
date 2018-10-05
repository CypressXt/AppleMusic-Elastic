# AppleMusic Elastic

## Description
  This project purpose is to import AppleMusic logged activity into Elasticsearch.

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
  Once you've the `Apple Music Play Activity.csv` file, use the `applemusic_to_es.py` script like this:
  ```
  ./applemusic_to_es.py [-h] -i CSV_INPUT_FILE -e ELASTIC_INDEX_URL
  ```

  Exemple:
  ```
  ./applemusic_to_es.py -i /myfolder/apple_music_play_activity.csv -e http://localhost:9200/applemusic-29.09.2018
  ```
