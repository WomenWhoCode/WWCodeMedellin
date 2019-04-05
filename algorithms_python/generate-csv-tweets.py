import tweepy #https://github.com/tweepy/tweepy
import csv
import twkeys

#Credenciales del Twitter API
consumer_key = twkeys.consumer_key()
consumer_secret = twkeys.consumer_secret()
access_key = twkeys.access_key()
access_secret = twkeys.access_secret()

#Remover los caracteres no imprimibles y los saltos de línea del texto del tweet
def strip_undesired_chars(tweet):
    #eliminar saltos de línea
    stripped_tweet = tweet.replace('\n', ' ').replace('\r', '')
    #eliminar caracteres extendidos
    char_list = [stripped_tweet[j] for j in range(len(stripped_tweet)) if ord(stripped_tweet[j]) in range(65536)]
    stripped_tweet=''
    for char in char_list:
        stripped_tweet=stripped_tweet+char
    return stripped_tweet

def get_all_tweets(screen_name):
    #Especificar aquí durante las pruebas un número entre 200 y 3240
    limit_number = 3240
    
    #Solicitar autorización a la app
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    
    #Inicializar arreglo vacío para descargar los tweets
    alltweets = []
    
    #Solicito descargar los primeros 200 tweets
    new_tweets = api.user_timeline(screen_name = screen_name,count=200)
    
    #Agregar los primeros 200
    alltweets.extend(new_tweets)
    
    #Registrar el ID del tweet 200 -1
    oldest = alltweets[-1].id - 1
    
    #Iniciamos el ciclo de descarga de los tweets
    while len(new_tweets) > 0 and len(alltweets) <= limit_number:
        #Anuncio de donde comienzan los tweets de esta descarga
        print ("getting tweets before" + str(oldest))
        
        #Traer tweets a partir del último descargado
        new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
        
        #agregar los tweets descargados
        alltweets.extend(new_tweets)
        
        #actualizar el ID del tweet más antiguo menos 1
        oldest = alltweets[-1].id - 1
        
        #imprimir número de tweets descargados en el arreglo en el momento
        print (str(len(alltweets)) + " tweets descargados hasta el momento")
        
    #creando un arreglo 2D con los datos que queremos de cada tweet
    outtweets = [(tweet.id_str, tweet.created_at, strip_undesired_chars(tweet.text),tweet.retweet_count,str(tweet.favorite_count)+'') for tweet in alltweets]

    #Crear el csv
    with open('%s_tweets.csv' % screen_name, "w", newline='') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerow(['id','created_at','text','retweet_count','favorite_count'''])
        writer.writerows(outtweets)
    pass
        

if __name__ == '__main__':
    #especificar el nombre de usuario de la cuenta a la cual se descargarán los tweets
    get_all_tweets("iyepes0120")

