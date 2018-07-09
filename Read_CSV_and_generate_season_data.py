import string
import statistics
import xlsxwriter

class Team(object):
	def __init__(self):
		self.name = ""
		self.points_scored = 0
		self.points_scored_list = []
		self.points_against = 0
		self.points_against_list = [] 
		self.games = []
		self.results = Results()
		self.statistics = Statistics()
		
class Results(object):
	def __init__(self):
		self.wins = 0
		self.losses = 0
		self.ties = 0 
	
class Statistics(object):
	def __init__(self):
		self.margins = []
		self.win_margins = []
		self.loss_margins = []
		self.margin_mean = 0
		self.margin_stdev = 0
		self.average_loss_margin = 0
		self.average_loss_margin_stdev = 0
		self.average_win_margin = 0
		self.average_win_margin_stdev = 0
		self.average_points_scored = 0
		self.average_points_scored_stdev = 0
		self.average_points_against = 0
		self.average_points_against_stdev = 0

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
			self.team_list = []
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
#			print ('name wins losses ties points_scored points_against margin_mean margin_stdev total_games')	

			for team in self.team_list:
				
				self.create_season_stats(team)
#				print (team.name, team.results.wins, team.results.losses, team.results.ties, team.points_scored, team.points_against, team.statistics.margin_mean, team.statistics.margin_stdev, team.results.wins+team.results.losses+team.results.ties)

			
		def calculate_one_season(self, season):
			self.clear()
			self.import_new_season(season)
			self.score_season()

		def calculate_one_old_season(self, season):
			self.clear()
			self.import_old_season(season)
			self.score_season()
		
		def calculate_all_seasons(self):
			self.clear()
			for season in (2012, 2013, 2014, 2015, 2016, 2017):
				self.import_new_season(season)
			for season in (2008, 2009, 2010, 2011):
				self.import_old_season(season)
			self.score_season()
			
		def count_result_for_game(self, team, game):
			self.add_scores_for_game(team, game)
			if game.result == 'WIN': 
				team.results.wins += 1
				self.add_margins_for_win(team, game)
			elif game.result == 'LOSS':
				team.results.losses += 1
				self.add_margins_for_loss(team, game)
			elif game.result == 'TIE':
				team.results.ties += 1
				self.add_margins_for_tie(team, game)

		def add_scores_for_game(self, team, game):
			team.points_scored += game.own_score
			team.points_scored_list.append(game.own_score)
			team.points_against += game.other_score
			team.points_against_list.append(game.other_score)
			
		def add_margins_for_win(self, team, game):
			team.statistics.margins.append(game.margin)
			team.statistics.win_margins.append(game.margin)
		
		def add_margins_for_loss(self, team, game):
			team.statistics.margins.append(game.margin)
			team.statistics.loss_margins.append(game.margin)
			
		def add_margins_for_tie(self, team, game):
			team.statistics.margins.append(game.margin)
				
				
		def create_season_stats(self, team):

			for game in team.games:
				self.count_result_for_game(team, game)
			self.calculate_statistics(team)
		
		def calculate_statistics(self, team):
			#print ('Hej: ', team.name)
			#print (team.statistics.win_margins)
			team.statistics.margin_mean = statistics.mean(team.statistics.margins)
			team.statistics.margin_mean = float("{0:.3f}".format(team.statistics.margin_mean))
			team.statistics.margin_stdev = statistics.stdev(team.statistics.margins)
			team.statistics.margin_stdev = float("{0:.3f}".format(team.statistics.margin_stdev))
			
			team.statistics.average_win_margin = statistics.mean(team.statistics.win_margins)
			team.statistics.average_win_margin = float("{0:.3f}".format(team.statistics.average_win_margin))
				
			if len(team.statistics.win_margins) > 1:
				team.statistics.average_win_margin_stdev = statistics.stdev(team.statistics.win_margins)
				team.statistics.average_win_margin_stdev = float("{0:.3f}".format(team.statistics.average_win_margin_stdev))
			else:
				team.statistics.average_win_margin_stdev = 0
			
			team.statistics.average_loss_margin = statistics.mean(team.statistics.loss_margins)
			team.statistics.average_loss_margin = float("{0:.3f}".format(team.statistics.average_loss_margin))
				
			if len(team.statistics.loss_margins) > 1:
				team.statistics.average_loss_margin_stdev = statistics.stdev(team.statistics.loss_margins)
				team.statistics.average_loss_margin_stdev = float("{0:.3f}".format(team.statistics.average_loss_margin_stdev))
			else:
				team.statistics.average_loss_margin_stdev = 0
				
			team.statistics.average_points_scored = statistics.mean(team.points_scored_list)
			team.statistics.average_points_scored = float("{0:.3f}".format(team.statistics.average_points_scored))
			team.statistics.average_points_scored_stdev = statistics.stdev(team.points_scored_list)
			team.statistics.average_points_scored_stdev = float("{0:.3f}".format(team.statistics.average_points_scored_stdev))
			
			team.statistics.average_points_against = statistics.mean(team.points_against_list)
			team.statistics.average_points_against = float("{0:.3f}".format(team.statistics.average_points_against))
			team.statistics.average_points_against_stdev = statistics.stdev(team.points_against_list)
			team.statistics.average_points_against_stdev = float("{0:.3f}".format(team.statistics.average_points_against_stdev))
			
			
		
		
		def write_to_xlsx(self):
			# Create a workbook and add a worksheet.
			workbook = xlsxwriter.Workbook('Resultat.xlsx')
			self.write_xlsx_sheet(workbook)
			workbook.close()
			
			
		def write_xlsx_sheet(self, workbook, name='Resultat'):
			print (name)
			worksheet = workbook.add_worksheet(str(name))
			row = 0
			col = 1
			# Start from the first cell. Rows and columns are zero indexed.
			worksheet.write(row, col-1,   'Year')
			worksheet.write(row, col,     'Team')
			worksheet.write(row, col + 1, 'Wins')
			worksheet.write(row, col + 2, 'Losses')
			worksheet.write(row, col + 3, 'Ties')
			worksheet.write(row, col + 4, 'Points scored')
			worksheet.write(row, col + 5, 'Points against')
			worksheet.write(row, col + 6, 'Margin mean')
			worksheet.write(row, col + 7, 'Margin stdev')
			worksheet.write(row, col + 8, 'Total games')
			worksheet.write(row, col + 9, 'Avg win margin')
			worksheet.write(row, col + 10, 'Avg win margin stdev')
			worksheet.write(row, col + 11, 'Avg loss margin')
			worksheet.write(row, col + 12, 'Avg loss margin stdev')
			worksheet.write(row, col + 13, 'Avg Points scored')
			worksheet.write(row, col + 14, 'Avg Points scored stdev')
			worksheet.write(row, col + 15, 'Avg Points against')
			worksheet.write(row, col + 16, 'Avg Points against stdev')
			row = 1
			# Iterate over the data and write it out row by row.
			for team in self.team_list:
				worksheet.write(row, col-1,   name)
				worksheet.write(row, col,     team.name)
				worksheet.write(row, col + 1, team.results.wins)
				worksheet.write(row, col + 2, team.results.losses)
				worksheet.write(row, col + 3, team.results.ties)
				worksheet.write(row, col + 4, team.points_scored)
				worksheet.write(row, col + 5, team.points_against)
				worksheet.write(row, col + 6, team.statistics.margin_mean)
				worksheet.write(row, col + 7, team.statistics.margin_stdev)
				worksheet.write(row, col + 8, team.results.wins+team.results.losses+team.results.ties)
				worksheet.write(row, col + 9, team.statistics.average_win_margin)
				worksheet.write(row, col + 10, team.statistics.average_win_margin_stdev)
				worksheet.write(row, col + 11, team.statistics.average_loss_margin)
				worksheet.write(row, col + 12, team.statistics.average_loss_margin_stdev)
				worksheet.write(row, col + 13, team.statistics.average_points_scored)
				worksheet.write(row, col + 14, team.statistics.average_points_scored_stdev)
				worksheet.write(row, col + 15, team.statistics.average_points_against)
				worksheet.write(row, col + 16, team.statistics.average_points_against_stdev)
						
				row += 1
				
				

		def calculate_all_seasons_individually_and_write_to_xlsx(self):
			workbook = xlsxwriter.Workbook('Resultat.xlsx')
			
			self.calculate_all_seasons()
			self.write_xlsx_sheet(workbook, 'Totalt')
			
			for season in (2017, 2016, 2015, 2014, 2013, 2012):
			#	print ('ÅR: ', season)
				self.calculate_one_season(season)
				self.write_xlsx_sheet(workbook, season)
			
			for season in (2011, 2010, 2009, 2008):
				self.calculate_one_old_season(season)
				self.write_xlsx_sheet(workbook, season)
				
			
				
			workbook.close()
			
if __name__ == "__main__":
		x = Worker()
#		x.calculate_one_season(2017)
#		x.calculate_all_seasons()
#		x.calculate_one_old_season(2011)
#		x.write_to_xlsx()
		x.calculate_all_seasons_individually_and_write_to_xlsx()

		
	