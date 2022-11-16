import yfinance as yf
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import reconstructor

db = SQLAlchemy()


class Asset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    ticker = db.Column(db.String(20), unique=True, nullable=False)

    def __init__(self, **kwargs):
        super(Asset, self).__init__(**kwargs)
        self.__init_on_load()

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.name}>"

    @reconstructor
    def __init_on_load(self):
        asset_in_db = Asset.query.filter_by(ticker=self.ticker).first()
        if asset_in_db is not None:
            self.id = asset_in_db.id

        self.__data_source = yf.Ticker(self.ticker)
        self.__price_history = dict()

        if self.id is not None:
            self.__load_prices_from_db()

    def __load_prices_from_db(self):
        prices = AssetPrice.query.filter_by(asset_id=self.id).all()

        for price in prices:
            self.__price_history[price.date] = price

    def fetch_prices(self, start_date, end_date=None, save_to_db=False):
        attr = ("open", "close", "low", "high")
        hist = self.__data_source.history(start=start_date, end=end_date)

        for price in hist.itertuples():
            date = price.Index.date()

            price_in_arr = self.__price_history.get(date)

            if price_in_arr is None:
                self.__price_history[date] = AssetPrice(
                    date=date,
                    asset_id=self.id,
                    **{x: getattr(price, x.capitalize()) for x in attr},
                )

                if save_to_db and self.id is not None:
                    db.session.add(self.__price_history[date])
            else:
                price_in_arr.__dict__.update(
                    ((x, getattr(price, x.capitalize())) for x in attr)
                )

        if save_to_db and self.id is not None:
            db.session.commit()

    @property
    def price_history(self):
        return self.__price_history


class AssetPrice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    open = db.Column(db.Float, nullable=False)
    close = db.Column(db.Float, nullable=False)
    low = db.Column(db.Float, nullable=False)
    high = db.Column(db.Float, nullable=False)
    asset_id = db.Column(db.Integer, db.ForeignKey("asset.id"), nullable=False)

    __table_args__ = (db.UniqueConstraint("asset_id", "date"),)
    attributes = ("id", "asset_id", "date", "open", "close", "low", "high")

    def __repr__(self):
        return f"<{self.__class__.__name__} " f"id={self.asset_id} date={self.date}>"

    def __len__(self):
        return len(self.attributes)

    def __iter__(self):
        for attr in self.attributes:
            yield getattr(self, attr)
