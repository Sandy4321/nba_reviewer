#!/usr/bin/env python
import urllib2
import json
import traceback
import datetime
import psycopg2
import sys
import nba as NBA

class Team(NBA.Configuration):

	all_imported = False

	def import_all_teams(self):
		print 'Start: Import NBA Teams'

		# First Game: 28th October 2014
		start_date = datetime.date(2014, 10, 28)
		# Last Game: 15th April 2015
		end_date = datetime.date(2015, 04, 15)

		# These are just some (random) dates.
		# When every NBA team has played his first home game, the team will be inserted in the nba_team table.
		# When this table has reached a size of 30 (all teams), the import will stop.
		
		dates = []
		delta = datetime.timedelta(days=1)
		while start_date <= end_date:
		    date = start_date.strftime("%Y%m%d")
		    dates.append(date)
		    start_date += delta

		try:
			for date in dates:
				if not self.all_imported:
					self.import_team(date)
				else:
					break
		except:
			print 'An error occured!'
			print traceback.print_exc();
		finally:
			print 'End:   Import NBA Teams' 


	def import_team(self, date):
		url = 'http://data.nba.com/json/cms/noseason/scoreboard/%s/games.json' % date
		data = self.get_data(url)
		
		self.con = psycopg2.connect(database='nba_reviewer', user='stijn') 
		self.cur = self.con.cursor() 
		self.write_team(data)


	def write_team(self, data):
		sports_content = data['sports_content']
		games = sports_content['games']
		if games:
			games = games['game']

			for game in games:

				try:

					self.cur.execute('SELECT count(1) FROM nba_team')
					size = self.cur.fetchone()

					print 'Table size %d' % size
					if size[0] == 30:
						self.all_imported = True
						break
					else:
						game_id = None
						self.cur.execute('SELECT team_id FROM nba_team WHERE team_id = \'%s\'' % game['home']['id'])
						game_id = self.cur.fetchone() # self.cur.fetchall()

						if game_id:
							print 'Update team'
							self.cur.execute('UPDATE nba_team SET city = \'%s\', nickname = \'%s\', team_id = \'%s\', key = \'%s\' WHERE team_id = \'%s\'' % 
												(game['home']['city'], game['home']['nickname'], game['home']['id'], game['home']['team_key'], game['home']['id']))
						else:
							print 'Insert team'
							self.cur.execute('INSERT INTO nba_team (city, nickname, team_id, key) VALUES (\'%s\', \'%s\', \'%s\', \'%s\')' % 
												(game['home']['city'], game['home']['nickname'], game['home']['id'], game['home']['team_key']))
						
						self.con.commit()

				except psycopg2.DatabaseError, e:
					if self.con:
						self.con.rollback()
					print 'Error %s' % e

			if self.con:		
				self.con.close()

t = Team()
t.import_all_teams()