from main_app.models import PageHit


class PageHitRouter:
    def db_for_read(self, model, **hints):
        if model == PageHit:
            return 'mongodb'

    def db_for_write(self, model, **hints):
        if model == PageHit:
            return 'mongodb'
