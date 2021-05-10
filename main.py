import download_subreddits
import logging
import build_user_subreddit_history
import build_genealogy_graph

logging.basicConfig(level=logging.INFO)

def main(subs, directory, start_date, end_date, num_founders = 50, edge_threshold = 0.1, 
                        days_diff = 7, is_comments = False):
    
    logging.info("downloading Reddit data from Pushshift")
    for sub in subs:
        download_subreddits.crawl_subreddit(sub, directory, start_date, end_date, comments = is_comments)
    
    logging.info("building user subreddit history")
    author_sub_timestamps_dic, sub_author_timestamps_dic, sub_founders_dic = \
            build_user_subreddit_history.build_user_subreddit_history(subs, 
                    founders = num_founders, comments = is_comments)
    
    logging.info("building genealogy graph")
    filename = build_genealogy_graph.get_parent_subs(sub_founders_dic, 
                        author_sub_timestamps_dic, directory = directory, days_diff = days_diff)
    
    logging.info("drawing genealogy graph")
    build_genealogy_graph.draw_graph(filename, "output.png", threshold = edge_threshold)
    

if __name__ == "__main__":
    start_date = '20200130'
    end_date = '20200315'
    num_founders = 50    
    edge_threshold = 0.1 
    days_diff = 7
    
    directory = "data/"
    
    COVID_regional_subs = ['CoronavirusUK', 
                  'CoronavirusUS', 
                  'CoronavirusDownunder',  
                  'CoronavirusWA', 
                  'CoronavirusCA', 
                  'CoronaVirusTX', 
                  'Coronavirus_Ireland', 
                  'CoronaVirusPA',
                  'Covid19_Ohio', 
                  'CoronavirusAZ', 
                  'CoronavirusNE', 
                  'CoronavirusMN', 
                  'CoronavirusMD', 
                  'CoronavirusMidwest',  
                  'CoronavirusSouth',  
                  'CoronavirusOregon', 
                  'coronavirusflorida',  
                  'CoronavirusJapan', 
                  'coronanetherlands', 
                  'Coronaviruslouisiana',   
                  'CoronavirusDACH', 
                  'CoronaVirus_ITALIA', 
                  'Coronavirus_NZ', 
                  'CoronavirusAlabama', 
                  'CoronavirusOklahoma', 
                  'CoronavirusTN']
    
    main(COVID_regional_subs, directory, start_date, end_date, num_founders = num_founders, 
        edge_threshold = edge_threshold, days_diff = days_diff, is_comments = False)
    