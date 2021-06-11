import twint
import datetime

def crawl(since, until):
    c = twint.Config()
    c.User_full     = True
    c.Profile_full  = True
    c.Stats         = True
    c.Store_csv     = True
    c.Hide_output   = True
#    c.Location      = True
    c.Hashtags      = True
#    c.Get_replies   = False
    c.Output        = "linkaja.csv"
    c.Search        = "linkaja"
    c.Limit         = 32000
    c.Lang          = "id"
    c.Since         = since
    c.Until         = until

    twint.run.Search(c)

if __name__ == "__main__":
    start_date  = datetime.datetime(2019, 7, 1, 0, 0)
    end_date    = datetime.datetime(2020, 10, 20, 0, 0)
    iter        = datetime.timedelta(days=0.5)
    while start_date <= end_date:
        crawl(str(start_date), str(start_date + iter))
        start_date += iter
