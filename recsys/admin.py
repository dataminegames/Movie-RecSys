from django.contrib import admin
from .models import *

from import_export.admin import ImportExportModelAdmin


class MovieInfoAdmin(ImportExportModelAdmin):
    search_fields = ['title']

class MovieChoiceAdmin(ImportExportModelAdmin):
    pass

class UserProfileAdmin(ImportExportModelAdmin):
    pass

class UserLikeAdmin(ImportExportModelAdmin):
    pass

admin.site.register(MovieInfo, MovieInfoAdmin)
admin.site.register(MovieChoice, MovieChoiceAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserLike, UserLikeAdmin)

