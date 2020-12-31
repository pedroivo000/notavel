import re
from notavel import db
from flask import request
from flask.views import MethodView
import notavel.models


class BaseView(MethodView):
    """Base class for MethodViewResolver views"""

    @property
    def model_name(self):
        """Get name of SQLAlchemy model class from child view class name"""
        return re.sub("sView", "", self.__class__.__name__)

    @property
    def schema_name(self):
        """Get name of Marshmallow schema class from child view class name"""

        return self.model_name + "Schema"

    def model(self, **kwargs):
        """Return instance of respective SQLAlchemy model for View class"""
        return getattr(notavel.models, self.model_name)(**kwargs)

    def schema(self, **kwargs):
        return getattr(notavel.models, self.schema_name)(**kwargs)

    def search(self, **kwargs):
        records = self.model().query.filter_by(**kwargs)
        return self.schema(many=True).dump(records), 200

    def get(self, **kwargs):
        # kwargs only contain a single element corresponding to resource id:
        id = list(kwargs.values())[0]
        record = self.model().query.get_or_404(id)

        return self.schema().dump(record), 200

    def post(self):
        body = request.json
        new_record = self.schema().load(body, session=db.session)
        db.session.add(new_record)
        db.session.commit()

        return self.schema().dump(new_record), 200

    def put(self, **kwargs):

        id = list(kwargs.values())[0]
        record = self.model().query.get_or_404(id)

        if record:
            body = request.json
            updated_record = self.schema().load(body, instance=record, partial=True)

        db.session.commit()

        return self.schema().dump(updated_record), 200

    def delete(self, **kwargs):

        id = list(kwargs.values())[0]
        record = self.model().query.get_or_404(id)

        db.session.delete(record)
        db.session.commit()

        return "", 204


class BulletsView(BaseView):
    pass


class ProjectsView(BaseView):
    pass


class NotesView(BaseView):
    pass
