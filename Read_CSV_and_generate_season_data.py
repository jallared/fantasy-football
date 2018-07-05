import string
import statistics
import csv

class Team(object):
	def __init__(self):
		self.name = ""
		self.wins = 0
		self.losses = 0
		self.ties = 0
		self.points_scored = 0
		self.points_against = 0
		self.margin_mean = 0
		self.margin_stdev = 0 
		self.games = []
	
class Game(object):
	def __init__(self):
		self.own_score = 0
		self.other_score = 0
		self.result = ''
		self.margin = 0
		
		
class Worker:
		def __init__(self):
			self.teams = ['Bagarmossen Barbarians','Danderyd Dragons','Gooberville Sea Lions',
							'GrÃ¶na Dalens VildhÃ¤star', 'Hjorthagen Highlanders','Lindesberg Latecomers',
							'Nya Englands Patrioter',"Saltis 73'ers",'Solna Big Moose','Vendelso Villains']
			self.season_file_map = {2012: 'Points & Margins - 2012.csv', 2013: 'Points & Margins - 2013.csv',
									2014: 'Points & Margins - 2014.csv', 2015: 'Points & Margins - 2015.csv', 
									2016: 'Points & Margins - 2016.csv', 2017: 'Points & Margins - 2017.csv'}
			self.old_season_file_map = {2008: 'Points & Margins - 2008.csv', 2009: 'Points & Margins - 2009.csv',
									2010: 'Points & Margins - 2010.csv', 2011: 'Points & Margins - 2011.csv'}
									
			self.team_list = []
			self.game_list = []
			
		def clear(self):
			self.game_list = []
			for name in self.teams:
				self.team_list.append(self.create_team(name))

			
		def create_team(self, name):
			team = Team()
			team.name = name
			return team

		def import_new_season(self, season):
			file_name = self.season_file_map[season]
			input = open(file_name, 'r')
			consume_or_not = ''
			for row in input:
				row = row.strip("\n").split("\t")
				if row[0].split(" ")[0] == 'PERIOD':
					consume_or_not = 'CONSUME'
				elif row[0].split(" ")[0] == 'SVENSKA':
					consume_or_not = 'NOT'
				else:
					if consume_or_not == 'CONSUME':
						self.game_list.append(row)

			input.close()

		def import_old_season(self, season):
			file_name = self.old_season_file_map[season]
			input = open(file_name, 'r')
			for row in input:
				row = row.strip("\n").split("\t")
				if (row[0][0] == 'W'):
					continue
				else:
					home_team, away_team = row[0].split(' at ')
					
					home_team, home_score = home_team.rsplit(" ",1)
					away_team, away_score = away_team.rsplit(" ",1)
				
				if home_score > away_score: 
					home_team += ' (W)'
					away_team += ' (L)'
				elif away_score > home_score:
					home_team += ' (L)'
					away_team += ' (W)'
				else: 
					home_team += ' (T)'
					away_team += ' (T)'
				score = str(home_score) + ' - ' + str(away_score)
				return_string = [home_team +',' + away_team + ',' + score + ',,']
				
				self.game_list.append(return_string)

			input.close()
		
			
		def read_results_for_one_game(self, game):
			game = game[0].split(',')
			home_team = game[0]
			away_team = game[1]
			home_score, away_score = game[2].split('-')
			home_score = int(float(home_score.strip()))
			away_score = int(float(away_score.strip()))
			home_team_result = home_team[-4:]
			home_team = home_team[:-4]
			away_team_result = away_team[-4:]
			away_team = away_team[:-4]

			

			for team in self.team_list:
				if home_team == team.name:
					game = Game()
					game.own_score = home_score
					game.other_score = away_score					
					game.margin = abs(game.own_score - game.other_score)
					if home_team_result == ' (W)':
						game.result = 'WIN'
					elif home_team_result == ' (L)':
						game.result = 'LOSS'
					elif home_team_result == ' (T)':
						game.result = 'TIE'
					team.games.append(game)
					
				elif away_team == team.name:
					game = Game()
					game.own_score = away_score
					game.other_score = home_score					
					game.margin = abs(game.own_score - game.other_score)
					if away_team_result == ' (W)':
						game.result = 'WIN'
					elif away_team_result == ' (L)':
						game.result = 'LOSS'
					elif away_team_result == ' (T)':
						game.result = 'TIE'
					team.games.append(game)

		def score_season(self):
			for game in self.game_list:
				self.read_results_for_one_game(game)
			print ('name wins losses ties points_scored points_against margin_mean margin_stdev total_games')	

			for team in self.team_list:
				
				self.create_season_stats(team)
				print (team.name, team.wins, team.losses, team.ties, team.points_scored, team.points_against, team.margin_mean, team.margin_stdev, team.wins+team.losses+team.ties)

			
		def calculate_one_season(self, season):
			self.clear()
			self.import_new_season(season)
			self.score_season()

		def calculate_one_old_season(self, season):
			self.clear()
			self.import_old_season(season)
			#self.score_season()
		
		def calculate_all_seasons(self):
			self.clear()
			for season in (2012, 2013, 2014, 2015, 2016, 2017):
				self.import_new_season(season)
			for season in (2008, 2009, 2010, 2011):
				self.import_old_season(season)
			self.score_season()
				
		def create_season_stats(self, team):
			margins = []
			for game in team.games:
				if game.result == 'WIN': 
					team.wins += 1
				elif game.result == 'LOSS':
					team.losses += 1
				elif game.result == 'TIE':
					team.ties += 1
					
				team.points_scored += game.own_score
				team.points_against += game.other_score
				margins.append(game.margin)

			team.margin_mean = statistics.mean(margins)
			team.margin_mean = float("{0:.3f}".format(team.margin_mean))
			team.margin_stdev = statistics.stdev(margins)
			team.margin_stdev = float("{0:.3f}".format(team.margin_stdev))
		
		def write_to_file(self):
#			input = open('Resultat', 'w')
			with open('Resultat.csv', 'w') as csvfile:
				spamwriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
				spamwriter.writerow(['team', 'wins', 'losses', 'ties', 'points_scored', 'points_against', 'margin_mean', 'margin_stdev', 'total_games'])	

				for team in self.team_list:
					spamwriter.writerow([team.name, team.wins, team.losses, team.ties, team.points_scored, team.points_against, team.margin_mean, team.margin_stdev, team.wins+team.losses+team.ties])

#			input.close()
		
if __name__ == "__main__":
		x = Worker()
#		x.calculate_one_season(2017)
		x.calculate_all_seasons()
#		x.calculate_one_old_season(2011)
		x.write_to_file()
	
		
	