from django.contrib import admin
from nba.models import Game, Team, GameComment, GameRating

class CommentInline(admin.TabularInline):
    model = GameComment
    extra = 1

class GameAdmin(admin.ModelAdmin):
	inlines = [CommentInline]
	search_fields = ['home', 'away', 'date']
	list_filter = ['date']

class TeamAdmin(admin.ModelAdmin):
	pass

class GameCommentAdmin(admin.ModelAdmin):
	pass

class GameRatingAdmin(admin.ModelAdmin):
	pass


admin.site.register(Game, GameAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(GameComment, GameCommentAdmin)
admin.site.register(GameRating, GameRatingAdmin)