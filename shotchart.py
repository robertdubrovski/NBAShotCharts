import requests
import numpy as np
from scipy.stats import binned_statistic_2d
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Arc
import seaborn as sns
import pylab
from matplotlib.offsetbox import OffsetImage
import urllib2 # should be "urllib.request", but iPython uses the python 2 version?



sns.set_style('white')
sns.set_color_codes()

class Chart:

    def __init__(self, playername, season, period=0, vsconference="",
                 seasontype="Regular Season", leagueid="00", lastngames=0,
                 teamid=0, position="", location="", outcome="", datefrom="",
                 contextmeasure="FGA", startperiod="", dateto="", endrange="",
                 opponentteamid=0, contextfilter="", rangetype="", month=0,
                 aheadbehind="", vsdivision="", pointdiff="", gameid="",
                 rookieyear="", gamesegment="", clutchtime="", startrange="",
                 endperiod="", seasonsegment="", playerposition=""):

        self.playername = playername.lower()

        self.season = season


        self.base_url = "http://stats.nba.com/stats/shotchartdetail?"

        self.parameters = {
            "playerid": get_player_id(playername),
            "Season": season,
            "period": period,
            "vsconference": vsconference,
            "seasontype": seasontype,
            "leagueid": leagueid,
            "lastngames": lastngames,
            "teamid": teamid,
            "position": position,
            "location": location,
            "outcome": outcome,
            "datefrom": datefrom,
            "contextmeasure": contextmeasure,
            "startperiod": startperiod,
            "dateto": dateto,
            "endrange": endrange,
            "opponentteamid": opponentteamid,
            "contextfilter": contextfilter,
            "rangetype": rangetype,
            "month": month,
            "aheadbehind": aheadbehind,
            "endrange": endrange,
            "vsdivision": vsdivision,
            "pointdiff": pointdiff,
            "rookieyear": rookieyear,
            "gamesegment": gamesegment,
            "startrange": startrange,
            "clutchtime": clutchtime,
            "gameid": gameid,
            "endperiod": endperiod,
            "seasonsegment": seasonsegment,
            "PlayerPosition": playerposition
        }

        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:39.0) Gecko/20100101 Firefox/39.0'}
        self.response = requests.get(self.base_url, params=self.parameters,
                headers=self.headers)

    def get_data(self):
        data = self.response.json()['resultSets'][0]['rowSet']
        headers = self.response.json()['resultSets'][0]['headers']
        return pd.DataFrame(data, columns=headers)

def get_player_id(player_name):
    url = "http://stats.nba.com/stats/commonallplayers?" + \
            "IsOnlyCurrentSeason=0&LeagueID=00&Season=2015-16"

    response = requests.get(url)
    playerList = response.json()['resultSets'][0]['rowSet']

    alist = player_name.split(" ")
    alist = alist[::-1]
    pname = ", ".join(alist)

    for player in playerList:
        if player[1].lower() == pname.lower():
            return player[0]

# Implement later
'''
def get_player_picture(player_id):

    url = "http://stats.nba.com/media/players/230x185/"+str(player_id)+".png"
    image = str(player_id) + ".png"
    return urllib2.request.urlretrieve(url, image)[0]
'''    

def draw_court(ax=None, color='gray', lw=1, outer_lines=False):
    """
    Returns an axes with a basketball court drawn onto to it.
    Function taken from tutorial by Savvas Tjortjoglou 

    This function draws a court based on the x and y-axis values that the NBA
    stats API provides for the shot chart data.  For example, the NBA stat API
    represents the center of the hoop at the (0,0) coordinate.  Twenty-two feet
    from the left of the center of the hoop in is represented by the (-220,0)
    coordinates.  So one foot equals +/-10 units on the x and y-axis.

    TODO: explain the parameters
    """
    if ax is None:
        ax = plt.gca()

    # Create the various parts of an NBA basketball court

    # Create the basketball hoop
    hoop = Circle((0, 0), radius=7.5, linewidth=lw, color=color, fill=False)

    # Create backboard
    backboard = Rectangle((-30, -7.5), 60, -1, linewidth=lw, color=color)

    # The paint
    # Create the outer box 0f the paint, width=16ft, height=19ft
    outer_box = Rectangle((-80, -47.5), 160, 190, linewidth=lw, color=color,
                          fill=False)
    # Create the inner box of the paint, widt=12ft, height=19ft
    inner_box = Rectangle((-60, -47.5), 120, 190, linewidth=lw, color=color,
                          fill=False)

    # Create free throw top arc
    top_free_throw = Arc((0, 142.5), 120, 120, theta1=0, theta2=180,
                         linewidth=lw, color=color, fill=False)
    # Create free throw bottom arc
    bottom_free_throw = Arc((0, 142.5), 120, 120, theta1=180, theta2=0,
                            linewidth=lw, color=color, linestyle='dashed')
    # Restricted Zone, it is an arc with 4ft radius from center of the hoop
    restricted = Arc((0, 0), 80, 80, theta1=0, theta2=180, linewidth=lw,
                     color=color)

    # Three point line
    # Create the right side 3pt lines, it's 14ft long before it arcs
    corner_three_a = Rectangle((-220, -47.5), 0, 140, linewidth=lw,
                               color=color)
    # Create the right side 3pt lines, it's 14ft long before it arcs
    corner_three_b = Rectangle((220, -47.5), 0, 140, linewidth=lw, color=color)
    # 3pt arc - center of arc will be the hoop, arc is 23'9" away from hoop
    three_arc = Arc((0, 0), 475, 475, theta1=22, theta2=158, linewidth=lw,
                    color=color)

    # Center Court
    center_outer_arc = Arc((0, 422.5), 120, 120, theta1=180, theta2=0,
                           linewidth=lw, color=color)
    center_inner_arc = Arc((0, 422.5), 40, 40, theta1=180, theta2=0,
                           linewidth=lw, color=color)

    # List of the court elements to be plotted onto the axes
    court_elements = [hoop, backboard, outer_box, inner_box, top_free_throw,
                      bottom_free_throw, restricted, corner_three_a,
                      corner_three_b, three_arc, center_outer_arc,
                      center_inner_arc]

    if outer_lines:
        # Draw the half court line, baseline and side out bound lines
        outer_lines = Rectangle((-250, -47.5), 500, 470, linewidth=lw,
                                color=color, fill=False)
        court_elements.append(outer_lines)

    # Add the court elements onto the axes
    for element in court_elements:
        ax.add_patch(element)

    return ax


def jointgrid(x, y, kind="scatter", data = None, title="", color="b",
              xlim=(-250, 250), ylim=(422.5,-47.5), court_color="gray",
              joint_color="b", marginals_color="b", chart = None,
              joint_kde_shade=True, marginals_kde_shade=True, court_lw=1, 
              joint_kws=None, marginal_kws=None, outer_lines=False, cmap=None,
              space=0, set_size_inches=(12,11), **kwargs):

    joint_kws = {}
    joint_kws.update(kwargs)

    marginal_kws = {}

    cmap = sns.light_palette(color, as_cmap=True)

    grid = sns.JointGrid(x,y, data=None, xlim=xlim, ylim=ylim, space=space)
    
    if kind=="kde":
        grid = grid.plot_joint(sns.kdeplot, cmap=cmap, shade=joint_kde_shade,
                               **joint_kws)
    else:
        grid = grid.plot_joint(plt.scatter, color=joint_color, **joint_kws)

    grid = grid.plot_marginals(sns.distplot, color=marginals_color,
            **marginal_kws)

    grid.fig.set_size_inches(set_size_inches)

    ax = grid.fig.get_axes()[0]

    ax.set_xlim(xlim)
    ax.set_ylim(ylim)

    draw_court(ax, color=court_color, lw=court_lw, outer_lines=outer_lines)

    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.tick_params(labelbottom="off", labelleft="off")

    title = chart.playername + " FGA \n" + chart.season + " Regular Season"

    ax.set_title(title, y=1.2, fontsize=18)



    return grid 

def display_charts():
    print("Enter player names as \'firstname lastname\', not case sensitive.")
    name = raw_input("Name of the player whose shot chart you wish to see: ")
    print("e.g. For the 2011-2012 NBA season, enter \'2011-12\'.")
    season = raw_input("From which season?: ")
    new = Chart(name, season)
    data = new.get_data()
    jointgrid(data.LOC_X, data.LOC_Y, chart=new)
    jointgrid(data.LOC_X, data.LOC_Y, "kde", chart=new)
    pylab.show()

display_charts()



