#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
from flask_migrate import Migrate
import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from forms import *
import sys
import datetime


#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')


# TODO: connect to a local postgresql database
# app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:petertalk@localhost:5434/fyurrdb'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


migrate = Migrate(app, db)




#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Show(db.Model):
  __tablename__ = 'show'
  id = db.Column(db.Integer, primary_key=True)
  artist_id = db.Column(db.ForeignKey('artist.id', ondelete='CASCADE'))
  venue_id =  db.Column(db.ForeignKey('venue.id',  ondelete='CASCADE'))
  start_time = db.Column(db.DateTime(), default=datetime.datetime.utcnow())
  





class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genre = db.Column(db.String())
    image_link = db.Column(db.String(500))
    website_link = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120))
    seeking_description = db.Column(db.String(500))
    seeking_talent = db.Column(db.Boolean, default=False)
    
    shows = db.relationship('Show', backref='venue', passive_deletes=True)
    
    
    
    
    @property
    def upcoming_shows(self):
      venue_shows = self.shows
  
      # Filter shows by artist id and datetime lesser than now
      filtered_shows_by_date = list(
        filter(lambda x: x.venue_id == self.id and x.start_time >= datetime.datetime.utcnow(), venue_shows)
      )
      
      shows = [show for show in filtered_shows_by_date]
      past_shows_for_venue = [
        {
          "artist_id": show.artist.id, 
          "artist_name": show.artist.name, 
          "artist_image_link":show.artist.image_link, 
          "start_time": show.start_time.strftime("%Y-%m-%d")
        } for show in shows
      ]
      
      return past_shows_for_venue
    
    
    @property
    def past_shows(self):
      
      venue_shows = self.shows
  
      # Filter shows by artist id and datetime greater than or equal to now
      filtered_shows_by_date = list(
        filter(lambda x: x.venue_id == self.id and x.start_time < datetime.datetime.utcnow(), venue_shows)
      )
      
      shows = [show for show in filtered_shows_by_date]
      past_shows_for_venue = [
        {
          "artist_id": show.artist.id, 
          "artist_name": show.artist.name, 
          "artist_image_link":show.artist.image_link, 
          "start_time": show.start_time.strftime("%Y-%m-%d")
        } for show in shows
      ]
      
      return past_shows_for_venue
    
    @property
    def past_shows_count(self):
      return len(self.past_shows)
    
    @property
    def upcoming_shows_count(self):
      return len(self.upcoming_shows)
      

    # TODO: implement any missing fields, as a database migration using Flask-Migrate




class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String())
    facebook_link = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    website_link = db.Column(db.String(120))
    seeking_description = db.Column(db.String(500))
    seeking_venue = db.Column(db.Boolean, default=False)
    
    shows = db.relationship('Show', backref='artist', passive_deletes=True)
    
    
    @property
    def past_shows(self):
      artist_shows = self.shows
  
      # Filter shows by artist id and datetime lesser than now
      filtered_shows_by_date = list(
        filter(lambda x: x.artist_id == self.id and x.start_time < datetime.datetime.utcnow(), artist_shows)
      )
      
      shows = [show for show in filtered_shows_by_date]
      past_shows_venues = [
        {
          "venue_id": show.venue.id, 
          "venue_name": show.venue.name, 
          "venue_image_link":show.venue.image_link, 
          "start_time": show.start_time.strftime("%Y-%m-%d")
        } for show in shows
      ]
      
      return past_shows_venues
    
    @property
    def upcoming_shows(self):
      artist_shows = self.shows
      
      # Filter shows by artist id and datetime greater than or equal to now
      filtered_shows_by_date = list(
        filter(lambda x: x.artist_id == self.id and x.start_time >= datetime.datetime.utcnow(), artist_shows)
      )
      
      shows = [show for show in filtered_shows_by_date]
      upcoming_shows_venues = [
        {
          "venue_id": show.venue.id, 
          "venue_name": show.venue.name, 
          "venue_image_link":show.venue.image_link, 
          "start_time": show.start_time.strftime("%Y-%m-%d")
        } for show in shows
      ]
      
      return upcoming_shows_venues
    
    
    @property
    def past_shows_count(self):
      return len(self.past_shows)
    
    @property
    def upcoming_shows_count(self):
      return len(self.upcoming_shows)
      
    

# TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.




#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime




#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')





#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
  venues_list = Venue.query.all()
  item = [(obj.state, obj.city) for obj in  venues_list]

  data = []

  for (state, city) in item:
      venues = Venue.query.filter_by(state=state)
      obj = {
          "city": city, 
          "state": state, 
          "venues": [
              {
                  "id": venue.id, 
                  "name": venue.name, 
                  "num_upcoming_shows": len([i for i in Venue.query.filter_by(name=venue.name)])
              } for venue in venues
          ]
      }
      
      data.append(obj)
  
  return render_template('pages/venues.html', areas=data)





@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on venues with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search_term=request.form.get('search_term', '').lower()
  
  print(search_term)
  
  venue_result = Venue.query.filter(Venue.name.ilike(f"%{search_term}%"))
  
  
  
  venue_result_list = [venue for venue in venue_result]
  print(venue_result_list)
  
  searched_data_list = [{
    "id": venue.id, 
    "name": venue.name, 
    "num_upcoming_shows": venue.upcoming_shows_count
  } for venue in venue_result_list]
  
  
  
  # Dummy Data for search
  response={
    "count": 0,
    "data": [
      {
        "id": 0,
        "name": "",
        "num_upcoming_shows": 0,
      }
    ]
  }
  # Update Dummy data with searched data instead
  response.update({"count": len(venue_result_list)})
  response.update({"data": searched_data_list})
  
  
  return render_template('pages/search_venues.html', results=response, search_term=search_term)




@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  venue = Venue.query.get(venue_id)
  
  data={
    "id": venue.id,
    "name": venue.name,
    "genres": json.loads(venue.genre),
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "website": venue.website_link,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "seeking_description": venue.seeking_description,
    "image_link": venue.image_link,
    "past_shows": venue.past_shows,
    "upcoming_shows": venue.upcoming_shows,
    "past_shows_count": venue.past_shows_count,
    "upcoming_shows_count": venue.upcoming_shows_count,
  }
  
  # data = list(filter(lambda d: d['id'] == venue_id, [data1, data2, data3]))[0]
  # return render_template('pages/show_venue.html', venue=data)
  return render_template('pages/show_venue.html', venue=data)




#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  
  return render_template('forms/new_venue.html', form=form)




@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  form = VenueForm(request.form)
  
  try:
    
    venue = Venue(
      name=form.name.data,
      city=form.city.data,
      state= form.state.data,
      address= form.address.data,
      phone=form.phone.data,
      genre=json.dumps(form.genres.data),
      facebook_link=form.facebook_link.data,
      image_link=form.image_link.data,
      website_link=form.website_link.data,
      seeking_talent=form.seeking_talent.data,
      seeking_description=form.seeking_description.data
    )
    
    db.session.add(venue)
    db.session.commit()
    
    # on successful db insert, flash success
    flash('Venue ' + form.name.data + ' was successfully listed!')
    
  except:
    print(sys.exc_info())
    db.session.rollback()
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    
    flash('An error occurred. Venue ' + form.name.data + ' could not be listed.')
  
  finally:
    db.session.close()
  
  return render_template('pages/home.html')




@app.route('/artists/delete/<artist_id>', methods=['DELETE', 'GET'])
def delete_artist(artist_id):
  # TODO: Complete this endpoint for taking a artist_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  try: 
    artist = Artist.query.get(artist_id)
    db.session.delete(artist)
    db.session.commit()
  except:
    db.session.rollback()
  finally: 
    db.session.close()
    
  
  # BONUS CHALLENGE: Implement a button to delete a artist on a artist Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return redirect(url_for('artists'))



@app.route('/venues/delete/<venue_id>', methods=['DELETE', 'GET'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  try: 
    venue = Venue.query.get(venue_id)
    db.session.delete(venue)
    db.session.commit()
  except:
    db.session.rollback()
  finally: 
    db.session.close()
    
  
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return redirect(url_for('venues'))




#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  artistData = Artist.query.all()
  data = [
    {
      "id": artist.id, 
      "name": artist.name
    } for artist in artistData
  ]
  

  return render_template('pages/artists.html', artists=data)




@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  
  search_term=request.form.get('search_term', '').lower()
  artist_result = Artist.query.filter(Artist.name.ilike(f"%{search_term}%"))
  
  artist_result_list = [artist for artist in artist_result]
  
  searched_data_list = [
    {
      "id": artist.id, 
      "name": artist.name, 
      "num_upcoming_shows": artist.upcoming_shows_count
    } for artist in artist_result_list
  ]
  
  # Dummy Data State for search
  response={
    "count": 0,
    "data": [
      {
        "id": 0,
        "name": "",
        "num_upcoming_shows": 0,
      }
    ]
  }
  
  
  # Update Dummy data with searched data instead
  response.update({"count": len(artist_result_list)})
  response.update({"data": searched_data_list})
    
  
  
  return render_template('pages/search_artists.html', results=response, search_term=search_term)




@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
  
  artist = Artist.query.get(artist_id)
  
  data={
    "id": artist.id,
    "name": artist.name,
    "genres": json.loads(artist.genres),
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website": artist.website_link,
    "facebook_link":  artist.facebook_link,
    "seeking_venue":  artist.phone,
    "seeking_description":  artist.seeking_description,
    "image_link":  artist.image_link,
    "past_shows":  artist.past_shows,
    "upcoming_shows":  artist.upcoming_shows,
    "past_shows_count":  artist.past_shows_count,
    "upcoming_shows_count":  artist.upcoming_shows_count,
  }
  
  return render_template('pages/show_artist.html', artist=data)




#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  
  # TODO: populate form with values from artist with ID <artist_id>
  
  data = Artist.query.get(artist_id)
  genre = json.dumps(data.genres)
  form = ArtistForm(obj=data)

  form.genres.data = genre
  
  
  artist={
    "id": data.id,
    "name": data.name,
    "genres": json.loads(data.genres),
    "city": data.city,
    "state": data.state,
    "phone": data.phone,
    "website": data.website_link,
    "facebook_link":  data.facebook_link,
    "seeking_venue":  data.phone,
    "seeking_description":  data.seeking_description,
    "image_link":  data.image_link,
  }
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)




@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  
  artist = Artist.query.get(artist_id)
  
  form = ArtistForm(request.form)

  try:
    artist.name=form.name.data
    artist.city=form.city.data
    artist.state= form.state.data
    artist.phone=form.phone.data
    artist.genres=json.dumps(form.genres.data)
    artist.facebook_link=form.facebook_link.data
    artist.image_link=form.image_link.data
    artist.website_link=form.website_link.data
    artist.seeking_venue=form.seeking_venue.data
    artist.seeking_description=form.seeking_description.data
  
    db.session.add(artist)
    db.session.commit()
    
    # on successful db insert, flash success
    flash('Artist ' + form.name.data + ' was successfully update!')
    
  except:
    print(sys.exc_info())
    db.session.rollback()
    
  finally:
    db.session.close()
  

  return redirect(url_for('show_artist', artist_id=artist_id))




@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  venue = Venue.query.get(venue_id)
  genre = json.dumps(venue.genre)
  # TODO: populate form with values from venue with ID <venue_id>
  form = VenueForm(obj=venue)
  form.genres.data = genre
  
  return render_template('forms/edit_venue.html', form=form, venue=venue)





@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  venue = Venue.query.get(venue_id)
  form = VenueForm(request.form)
  
  try:
    venue.name=form.name.data
    venue.city=form.city.data
    venue.state= form.state.data
    venue.address= form.address.data
    venue.phone=form.phone.data
    venue.genre=json.dumps(form.genres.data)
    venue.facebook_link=form.facebook_link.data
    venue.image_link=form.image_link.data
    venue.website_link=form.website_link.data
    venue.seeking_talent=form.seeking_talent.data
    venue.seeking_description=form.seeking_description.data
    
    print(venue.seeking_talent)
    
    db.session.add(venue)
    db.session.commit()
    
    # on successful db insert, flash success
    flash('Venue ' + form.name.data + ' was successfully update!')
    
  except:
    print(sys.exc_info())
    db.session.rollback()
    flash('Venue ' + form.name.data + ' was not successfully update!')
    
  finally:
    db.session.close()
  
  
  return redirect(url_for('show_venue', venue_id=venue_id))




#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  form = ArtistForm(request.form)
  
  try:
    artist = Artist(
        name=form.name.data,
        city=form.city.data,
        state= form.state.data,
        phone=form.phone.data,
        genres=json.dumps(form.genres.data),
        facebook_link=form.facebook_link.data,
        image_link=form.image_link.data,
        website_link=form.website_link.data,
        seeking_description=form.seeking_description.data,
        seeking_venue=form.seeking_venue.data
    )
    
    db.session.add(artist)
    db.session.commit()
    flash('Artist ' + request.form.get('name') + ' was successfully listed!')
    
  except:
    db.session.rollback()
    print(sys.exc_info())
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    flash('An error occurred. Artist ' + request.form.get('name') + ' could not be listed.')
  
  finally:
    db.session.close()
    
  
  # on successful db insert, flash success
  return render_template('pages/home.html')





#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  
  shows = Show.query.all()
  
  data = [
    {
      "venue_id": show.venue_id,
      "venue_name": show.venue.name,
      "artist_id": show.artist_id,
      "artist_name": show.artist.name,
      "artist_image_link": show.artist.image_link,
      "start_time": show.start_time.strftime("%Y-%m-%d")
    } for show in shows
  ]
  
  
  
  return render_template('pages/shows.html', shows=data)




@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)




@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  form = ShowForm(request.form)
  
  # Custom check to know if artist_id and venue_id exists
  venue_ids = [ venue.id for venue in Venue.query.all() ]
  artist_ids = [ venue.id for venue in Venue.query.all() ]

  try:
    
    show = Show(
      artist_id=form.artist_id.data,
      venue_id=form.venue_id.data,
      start_time=form.start_time.data
    )
    if int(show.venue_id) not in venue_ids:
      raise ValueError("Venue ID does not exist... ")
      
    if int(show.artist_id) not in artist_ids:
      raise ValueError("Artist ID does not exist... ")
      
    
    db.session.add(show)
    db.session.commit()
    
    
    # on successful db insert, flash success
    flash('Show was successfully listed!')
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  except ValueError:
    db.session.rollback()
    flash('An error occurred. Show could not be listed.')
  finally:
    db.session.close()
  
  return render_template('pages/home.html')





@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404




@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500





if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')




#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()




# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
