from django.contrib import admin
from nba.models import Game, Team, Comment, CommentCategory

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1

class GameAdmin(admin.ModelAdmin):
	inlines = [CommentInline]
	search_fields = ['home', 'away', 'date']
	list_filter = ['date']

class TeamAdmin(admin.ModelAdmin):
	pass

class CommentAdmin(admin.ModelAdmin):
	pass

class CommentCategoryAdmin(admin.ModelAdmin):
	pass


admin.site.register(Game, GameAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(CommentCategory, CommentCategoryAdmin)