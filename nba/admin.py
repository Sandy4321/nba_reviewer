from django.contrib import admin
from nba.models import Game, Team, GameComment, GameRating, GamePerUser

class CommentInline(admin.TabularInline):
    model = GameComment
    extra = 1

class GameAdmin(admin.ModelAdmin):
	inlines = [CommentInline]
	search_fields = ['home', 'away', 'date']
	list_filter = ['date']

admin.site.register(Game, GameAdmin)
admin.site.register(Team,)
admin.site.register(GameComment,)
admin.site.register(GameRating)
admin.site.register(GamePerUser)