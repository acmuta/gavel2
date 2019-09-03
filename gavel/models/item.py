from gavel.models import db
import gavel.crowd_bt as crowd_bt
from sqlalchemy.orm.exc import NoResultFound

from gavel.models._basemodel import BaseModel

view_table = db.Table('view',
                      db.Column('item_id', db.Integer, db.ForeignKey('item.id')),
                      db.Column('annotator_id', db.Integer, db.ForeignKey('annotator.id'))
                      )


class Item(BaseModel):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.Text, nullable=False)
    location = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    active = db.Column(db.Boolean, default=True, nullable=False)
    viewed = db.relationship('Annotator', secondary=view_table)
    prioritized = db.Column(db.Boolean, default=False, nullable=False)
    flags = db.relationship('Flag', back_populates="item")

    mu = db.Column(db.Float)
    sigma_sq = db.Column(db.Float)

    _default_fields = ["name", "location", "description", "active", "seen", "prioritized", "mu", "sigma_sq"]

    relations_keys = ("viewed", "flags")

    def __init__(self, name, location, description):
        self.name = name
        self.location = location
        self.description = description
        self.mu = crowd_bt.MU_PRIOR
        self.sigma_sq = crowd_bt.SIGMA_SQ_PRIOR

    @property
    def seen(self):
        return len(self.viewed)

    @classmethod
    def by_id(cls, uid):
        if uid is None:
            return None
        try:
            item = cls.query.get(uid)
        except NoResultFound:
            item = None
        return item
