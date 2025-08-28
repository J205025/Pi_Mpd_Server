# main.py
# This script creates a FastAPI application to expose API endpoints
# for controlling the Music Player Daemon (MPD).
import os
import json # Added for JSON handling
from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
from typing import Optional, List # Added List
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from pathlib import Path
from my_package.mpd_controller import MPDClientController
from my_package.database import get_db
from my_package.models import User, UserPlaylist # Added UserPlaylist
# Updated imports to include PlaylistPayload
from my_package.schemas import UserCreate, UserResponse, Token, UserPlaylistCreate, UserPlaylistResponse, PlaylistPayload, PlaylistsListResponse
from my_package.auth import get_password_hash, verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, get_current_user
import uvicorn
from contextlib import asynccontextmanager
from my_package.database import Base, engine
# ----------------------------------------------
music_Basefolder = "/home/ubuntu/Music/"
music_Type= ["國語","台語","英語","古典","播客"]
folderpath = Path(music_Basefolder+music_Type[0])
artist = [item.name for item in folderpath.iterdir() if item.is_dir()]
#-----------------------------------------------
pi_ALLFILES = [] 
pi_Playlist_List = []  # Only one pi_Playlist_List for Pi_Server
pi_playlist_files = []
pi_IndexMax = 1
pi_Index = 0
pi_Playing = None
pi_Playmode = None
pi_RadioNo = None
pi_Volume = 1
pi_Mute = False
pi_Playrate = 1
pi_Duration = 0
cron_Status =  False
cron_Hour = '00'
cron_Min = '00'
cron_pi_Index = 1
pc_ALLFILES = []
pc_Playlist_List = [] # Each user will have his own pc_Playlist_List
pc_Playlist_files = []
pc_Indexmax = 1

# Initialize the MPD client controller globally
mpd_player = MPDClientController()

MPD_PLAYMODE = ["repeat", "random", "single", "consume"]
RADIO_STREAMS = {
    "BBCWorldService": "https://stream.live.vc.bbcmedia.co.uk/bbc_world_service",
    "ClassicFM": "https://media-the.musicradio.com/ClassicFM",
    "LBCLondon": "https://media-ssl.musicradio.com/LBCLondon",
    "TimesRadio": "https://timesradio.wireless.radio/stream",
    "url01":"https://stream.live.vc.bbcmedia.co.uk/bbc_world_service",
    "url02":"http://stream.live.vc.bbcmedia.co.uk/bbc_london",
    "url03":"https://npr-ice.streamguys1.com/live.mp3",
    "url04":"https://prod-18-232-88-129.wostreaming.net/foxnewsradio-foxnewsradioaac-imc?session-id=0f99acd44126cef33b40ce217c9ea1ad",
    "url05":"http://stream.live.vc.bbcmedia.co.uk/bbc_radio_five_live",
    "url06":"http://stream.live.vc.bbcmedia.co.uk/bbc_asian_network",
    "url07":"http://stream.live.vc.bbcmedia.co.uk/bbc_radio_one",
    "url08":"https://icrt.leanstream.co/ICRTFM-MP3?args=web",
    "url09":"http://stream.live.vc.bbcmedia.co.uk/bbc_radio_two",
    "url10":"http://localhost:8000/stream.ogg",
    "url11":"http://onair.family977.com.tw:8000/live.mp3",
    "url12":"https://n09.rcs.revma.com/aw9uqyxy2tzuv?rj-ttl=5&rj-tok=AAABhZollCEACdvxzVVN61ARVg",
    "url13":"https://n10.rcs.revma.com/ndk05tyy2tzuv?rj-ttl=5&rj-tok=AAABhZouFPAAQudE3-49-1PFHQ",
    "url14":"https://n09.rcs.revma.com/7mnq8rt7k5zuv?rj-ttl=5&rj-tok=AAABhZovh0cASZAucd0xcmxkvQ",
    "url15":"https://n11a-eu.rcs.revma.com/em90w4aeewzuv?rj-tok=AAABhZoyef8AtFfbdaYYtKJnaw&rj-ttl=5",
    "url16":"https://n07.rcs.revma.com/78fm9wyy2tzuv?rj-ttl=5&rj-tok=AAABhZozdbQAkV-tPDO6A5aHag",
    "url17":"http://stream.live.vc.bbcmedia.co.uk/bbc_radio_three",
    "url18":"http://stream.live.vc.bbcmedia.co.uk/bbc_radio_fourfm",
    "url19":"http://stream.live.vc.bbcmedia.co.uk/bbc_6music",
    "url30":"http://media-ice.musicradio.com:80/ClassicFMMP3"
}

# Generate filespath base from music_Basefolder
def genFilelist(subfolder):
    global pc_Indexmax
    global music_Basefolder
    
    songs = []; 
    for path, subdirs, files in os.walk(music_Basefolder + subfolder, followlinks=True):
       # for name in files:
        path = path[(len(music_Basefolder)-1):]
        path = path+"/"
        path = path[1:]
        files = [path + file for file in files]
        songs = songs + files; 
    songs = [ f for f in songs if f[-4:] == '.mp3' or f[-4:] =='.MP3' or f[-5:] == '.flac' or f[-5:] == '.FLAC']
    songs.sort()
    return songs

# --- FastAPI App  Setup ---
# --- Application Lifespan Event Handler ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    global music_Type
    global pi_ALLFILES  
    global pc_ALLFILES
    """
    Handles application startup and shutdown events.
    This replaces the deprecated @app.on_event("startup") and @app.on_event("shutdown").
    """
    print("Application startup...")
    # Create database tables
    Base.metadata.create_all(bind=engine)
    # Connect to the MPD server before the application starts
    mpd_player.connect()

    if not mpd_player.is_connected:
        raise HTTPException(status_code=503, detail="MPD is not connected")
   #Update the music database and save to playlist
    mpd_player.update()
    mpd_player.queue_clear()
    mpd_player.queue_add_folder(music_Type[0])
    mpd_player.queue_saveto_playlist(music_Type[0])
    mpd_player.queue_clear()
    mpd_player.queue_add_folder(music_Type[1])
    mpd_player.queue_saveto_playlist(music_Type[1])
    mpd_player.queue_clear()
    mpd_player.queue_add_folder(music_Type[2])
    mpd_player.queue_saveto_playlist(music_Type[2])
    mpd_player.queue_clear()
    mpd_player.queue_add_folder(music_Type[3])
    mpd_player.queue_saveto_playlist(music_Type[3])
    mpd_player.queue_clear()
    mpd_player.queue_add_folder(music_Type[4])
    mpd_player.queue_saveto_playlist(music_Type[4])
    mpd_player.queue_clear()
    mpd_player.queue_load_radiostreams(RADIO_STREAMS)
    mpd_player.queue_saveto_playlist("廣播")

    #When fastapi starts,  it generate pc_playist_ALL
    pc_ALLFILES = genFilelist("")
    print(f"--- Found {len(pc_ALLFILES)} songs for PC ALLFILEs.")
    ####print("ALL songs in Music_BaseFolder_Pc:"+str(pc_PLAYLIST_ALL))
    try:
        # The `yield` statement indicates that the application is ready to serve requests
        yield
    finally:
        # Disconnect from the MPD server after the application shuts down
        print("Application shutdown...")
        mpd_player.disconnect()
  
# Initialize FastAPI application
# Configure CORS (Cross-Origin Resource Sharing)
# This allows the frontend (running on a different origin) to make requests to the backend.
origins = [
    "http://localhost:3000",  # The default address for a Vite dev server
    "http://127.0.0.1:3000",
    "*"
]
app = FastAPI(lifespan=lifespan,
    title="MPD Player API",
    description="A Player with Music Player Daemon (MPD).",
    version="1.0.0"
)

# Path to your built Nuxt.js application
NUXT_DIST_PATH = Path("../frontend/.output/public")  # Adjust path as needed

# Check if Nuxt build exists
if not NUXT_DIST_PATH.exists():
    raise Exception(f"Nuxt build not found at {NUXT_DIST_PATH}. Run 'npm run build' in your Nuxt project first.")

# Mount static files - ORDER MATTERS!
# 1. Mount your backend static files first with a specific prefix
app.mount("/static", StaticFiles(directory="static"), name="backend_static")  # Your backend static files

# 2. Mount Nuxt assets and the entire public directory
app.mount("/_nuxt", StaticFiles(directory=NUXT_DIST_PATH / "_nuxt"), name="nuxt_assets")
# 3. Mount music files
app.mount("/music", StaticFiles(directory="/home/ubuntu/Music"), name="music_files")
# 4. Mount image files
app.mount("/images", StaticFiles(directory=NUXT_DIST_PATH / "images"), name="nuxt_images")
# 5. Mount the entire Nuxt public directory to serve all static files including _payload.json
app.mount("/app", StaticFiles(directory=NUXT_DIST_PATH, html=True), name="nuxt_app")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows specified origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)


# --- API Endpoints ---
# Serve the main index.html file for the root path
@app.get("/favicon.ico")
async def favicon():
    return FileResponse(os.path.join("static", "favicon.ico"))

@app.get("/")
async def root():
    """
    Serve the root route
    """
    index_file = NUXT_DIST_PATH / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    else:
        return HTMLResponse("<h1>Welcome! Nuxt app not found.</h1>")

# Handle _payload.json requests specifically
@app.get("/_payload.json")
async def serve_payload():
    """
    Serve the main _payload.json file
    """
    payload_file = NUXT_DIST_PATH / "_payload.json"
    if payload_file.exists():
        return FileResponse(payload_file, media_type="application/json")
    else:
        # Return empty payload if file doesn't exist
        return JSONResponse({})

# Handle dynamic _payload.json requests with query parameters
@app.get("/{path:path}/_payload.json")
async def serve_dynamic_payload(path: str):
    """
    Serve dynamic _payload.json files for specific routes
    """
    # Try to find the specific payload file
    payload_file = NUXT_DIST_PATH / path / "_payload.json"
    if payload_file.exists():
        return FileResponse(payload_file, media_type="application/json")
    
    # Fallback to main payload
    main_payload = NUXT_DIST_PATH / "_payload.json"
    if main_payload.exists():
        return FileResponse(main_payload, media_type="application/json")
    
    # Return empty payload if no file exists
    return JSONResponse({})

# API routes - make sure all your API routes are defined BEFORE the catch-all route
@app.post('/')
async def index_post():
    global pc_PLAYLIST_ALL
    global pi_PLAYLIST_ALL
    global pi_Index
    global pi_Playing
    global pi_Playmode
    global pi_RadioNo
    global pi_Volume
    global pi_Mute
    global pi_Playrate
    global pi_Duration
    global cron_Status
    global cron_Hour
    global cron_Min
    global cron_pi_Index
    return JSONResponse({
        "pc_Playlist" : pc_ALLFILES,
        "pi_Playlist" : pi_ALLFILES,
        "pi_Index" : pi_Index,
        "pi_Playing" : pi_Playing,
        "pi_Playmopde" : pi_Playmode,
        "pi_RadioNo" : pi_RadioNo,
        "pi_Volume" : pi_Volume,
        "pi_Mute" : pi_Mute,
        "pi_Playrate" : pi_Playrate,
        "pi_Duration" : pi_Duration,
        "cronStatus" : cron_Status,
        "cronTimeHour" : cron_Hour,
        "cronTimeMin" : cron_Min,
        "cronIndexPi" : cron_pi_Index
         })

@app.get("/status")
async def get_pi_status():
    """
    Returns the current status of the MPD player.
    """
    if not mpd_player.is_connected:
        raise HTTPException(status_code=503, detail="MPD is not connected")
    
    status = mpd_player.get_status()
    if status is None:
        raise HTTPException(status_code=500, detail="Failed to retrieve status")
    
    return status

@app.get("/pi_get_playlist/")
async def pi_get_playlist():
    """
    Get playlist in Queue
    """
    if not mpd_player.is_connected:
        raise HTTPException(status_code=503, detail="MPD is not connected")
    try:
            
        playlist = mpd_player.get_playlist()
        return playlist
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving playplaylist: {e}") 

@app.get("/pi_get_playlistid/")
async def pi_get_playlistid():
    """
    Get playlist in Queue
    """
    if not mpd_player.is_connected:
        raise HTTPException(status_code=503, detail="MPD is not connected")
    try:
            
        playlistid = mpd_player.get_playlisid()
        return playlistid
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving playplaylist: {e}") 

@app.get("/pi_gen_playlist/{foldername}")
async def pi_gen_playlist(folder_name:str):
    """
    Generate a  playlist and save to  Queue
    """
    if not mpd_player.is_connected:
        raise HTTPException(status_code=503, detail="MPD is not connected")
    try:
            
        playlist = mpd_player.queue_add_folder(folder_name)
        return playlist
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving playplaylist: {e}") 
    
#TTTok
@app.get("/pi_load_from_playlist/{pi_plname}")
async def pi_load_from_playlist(pi_plname:str):
    """
    Find if pi_plname in playlists list, and load to Queue
    """
    if not mpd_player.is_connected:
        raise HTTPException(status_code=503, detail="MPD is not connected")
    try:
            
        mpd_player.queue_loadfrom_playlist(pi_plname)
        return {"message": "Loading '{pi_plname}'."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading playlist: {e}")
    
#TTT
@app.get("/pi_save_to_playlist/{pi_plname}")
async def save_pi_playlist_current(pi_plname:str):
    """
    Save current Queue to mpd playlist
    """
    if not mpd_player.is_connected:
        raise HTTPException(status_code=503, detail="MPD is not connected")
    try:
            
        mpd_player.queue_saveto_playlist(pi_plname)
        return {"message": "Playlist saved."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving playplaylist: {e}")
#    
@app.get("/pi_get_playlists_list")
async def get_playlists_list():
    """
    Get  playlists list.
    """
    try:
        pi_playlists_list = mpd_player.get_playlists_list()
        return pi_playlists_list 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting playlists list: {e}")    

@app.post("/pi_play")
async def pi_play():
    """
    Starts or resumes music playback.
    """
    if not mpd_player.is_connected:
        raise HTTPException(status_code=503, detail="MPD is not connected")
    
    try:
        mpd_player.play()
        return {"message": "Playback started."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error playing music: {e}")
    
@app.post("/pi_playid/{song_id}")
async def pi_playid(song_id: str):
    """
    Selects a song from the playlist and starts playing it.
    The song_id is the position in the playlist (0-indexed).
    """
    if not mpd_player.is_connected:
        raise HTTPException(status_code=503, detail="MPD is not connected")
    
    try:
        mpd_player.client.playid(song_id)
        return {"message": f"Playing song with id {song_id}."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error selecting and playing song: {e}")

@app.post("/pi_pause")
async def pi_pause():
    """
    Pauses or unpauses music playback.
    """
    if not mpd_player.is_connected:
        raise HTTPException(status_code=503, detail="MPD is not connected")
    
    try:
        mpd_player.pause()
        return {"message": "Playback paused/unpaused."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error pausing music: {e}")

@app.post("/pi_stop")
async def pi_stop():
    """
    Stops music playback.
    """
    if not mpd_player.is_connected:
        raise HTTPException(status_code=503, detail="MPD is not connected")
    
    try:
        mpd_player.stop()
        return {"message": "Playback stopped."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error stopping music: {e}")

@app.post("/pi_next")
async def pi_next():
    """
    Skips to the next song in the playlist.
    """
    if not mpd_player.is_connected:
        raise HTTPException(status_code=503, detail="MPD is not connected")
    
    try:
        mpd_player.next()
        return {"message": "Skipped to the next song."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error skipping to next song: {e}")

@app.post("/pi_prev")
async def pi_prev():
    """
    Goes back to the previous song in the playlist.
    """
    if not mpd_player.is_connected:
        raise HTTPException(status_code=503, detail="MPD is not connected")
    
    try:
        mpd_player.prev()
        return {"message": "Skipped to the previous song."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error skipping to previous song: {e}")

@app.put("/pi_setvolume/{volume}")
async def pi_setvol(volume: int):
    """
    Sets the volume of the MPD player.
    """
    if not mpd_player.is_connected:
        raise HTTPException(status_code=503, detail="MPD is not connected")
    
    if not 0 <= volume <= 100:
        raise HTTPException(status_code=400, detail="Volume must be an integer between 0 and 100.")
    
    try:
        mpd_player.setvolume(volume)
        return {"message": f"Volume set to {volume}."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error setting volume: {e}")

@app.put("/pi_playmode")
async def pi_playmode(repeat: Optional[bool] = None, random: Optional[bool] = None, single: Optional[bool] = None):
    """
    Sets the play mode of the MPD player (repeat, shuffle, single).
    """
    if not mpd_player.is_connected:
        raise HTTPException(status_code=503, detail="MPD is not connected")
    
    try:
        if repeat is not None:
            mpd_player.client.repeat(1 if repeat else 0)
        if random is not None:
            mpd_player.client.random(1 if random else 0)
        if single is not None:
            mpd_player.client.single(1 if single else 0)
        
        return {"message": "Play mode updated."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error setting play mode: {e}")

# Pcplayer API 
@app.get("/pc_get_playlist_List", response_model=PlaylistsListResponse)
async def pc_get_playlists_list(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieves a list of all playlist names for the current user.
    """
    # Query the database for playlist names belonging to the current user
    playlist_names_tuples = db.query(UserPlaylist.playlist_name).filter(UserPlaylist.user_id == current_user.id).all()
    
    # The query returns a list of tuples, e.g., [('playlist1',), ('playlist2',)].
    # We need to flatten it into a simple list of strings.
    playlist_names = [name for (name,) in playlist_names_tuples]
    
    return {"names": playlist_names}

@app.get("/pc_get_playlist_files/{pc_plname}")
async def pc_get_playlist_files(
    pc_plname :str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)

):
    """
    Retrieves a specific playlist for the current user.
    """
    user_playlist = db.query(UserPlaylist).filter(
        UserPlaylist.user_id == current_user.id,
        UserPlaylist.playlist_name == pc_plname
    ).first()

    if user_playlist:
        # The data is stored as a JSON string, so we need to parse it back into a list
        return json.loads(user_playlist.playlist_data)
    
    # If no playlist is found, return an empty list
    return []

@app.post("/pc_save_playlists_tolist/{pc_plname}")
async def pc_save_playlist_files(
    pc_plname: str, # Captures the playlist name from the URL path
    payload: PlaylistPayload, # Uses the Pydantic model for the request body
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Saves or updates a playlist for the currently authenticated user.
    - pc_plname: The name of the playlist to save.
    - payload: The request body containing the list of songs.
    """
    # Check if a playlist with this name already exists for this user
    user_playlist = db.query(UserPlaylist).filter(
        UserPlaylist.user_id == current_user.id,
        UserPlaylist.playlist_name == pc_plname
    ).first()

    # Convert the list of songs into a JSON string for storage
    playlist_data_json = json.dumps(payload.songs)

    if user_playlist:
        # If it exists, update the playlist data
        user_playlist.playlist_data = playlist_data_json
        db.commit()
        db.refresh(user_playlist)
        return {"message": f"Playlist '{pc_plname}' updated successfully"}
    else:
        # If it does not exist, create a new playlist entry
        new_playlist = UserPlaylist(
            user_id=current_user.id,
            playlist_name=pc_plname,
            playlist_data=playlist_data_json
        )
        db.add(new_playlist)
        db.commit()
        db.refresh(new_playlist)
        return {"message": f"Playlist '{pc_plname}' created successfully"}

@app.delete("/pc_delete_playlist_list/{pc_plname}")
async def pc_delete_playlist_list(
    pc_plname: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Deletes a specific playlist for the current user.
    - pc_plname: The name of the playlist to delete.
    """
    # Query the database for the specific playlist belonging to the current user
    playlist_to_delete = db.query(UserPlaylist).filter(
        UserPlaylist.user_id == current_user.id,
        UserPlaylist.playlist_name == pc_plname
    ).first()

    # If the playlist doesn't exist, raise a 404 Not Found error
    if not playlist_to_delete:
        raise HTTPException(status_code=404, detail=f"Playlist '{pc_plname}' not found")

    # Delete the playlist from the database session
    db.delete(playlist_to_delete)
    # Commit the transaction to make the deletion permanent
    db.commit()

    return {"message": f"Playlist '{pc_plname}' deleted successfully"}


@app.get("/pc_get_allfiles")
async def pc_get_allfiles():
    #global pc_ALLFILES
    #print("/pc_get_allfiles:"+ str(pc_ALLFILES))
    files = [""]
    return files

@app.get("/pc_gen_fileslist/{foldername}")
async def pc_gen_fileslist(
    foldername :str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):   
    fileslist = genFilelist(foldername)
    return fileslist
#------------------------------------------------------------------------------
# User Management
@app.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Define your designated registration code
    # For better security, load this from an environment variable
    DESIGNATED_CODE = "Happy"

    # Check if the provided code matches
    if user.code != DESIGNATED_CODE:
        raise HTTPException(status_code=400, detail="Invalid registration code")
    
    # Check if the username is already registered
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # Proceed with user creation
    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me/", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


# IMPORTANT: This catch-all route MUST be the LAST route defined
# It handles all SPA routes that don't match API endpoints or static files
@app.get("/{full_path:path}")
async def catch_all(full_path: str):
    """
    Catch-all route to serve index.html for all SPA routes
    This ensures that client-side routing works properly
    """
    # Skip API routes and static assets
    if full_path.startswith(("api/", "_nuxt/", "music/", "static/", "app/")):
        raise HTTPException(status_code=404, detail="Not found")
    
    # Skip _payload.json requests (they should be handled by specific routes above)
    if full_path.endswith("_payload.json"):
        raise HTTPException(status_code=404, detail="Payload not found")
    
    # Skip files with extensions (likely static files)
    if "." in full_path.split("/")[-1] and not full_path.endswith(".html"):
        raise HTTPException(status_code=404, detail="Not found")
    
    index_file = NUXT_DIST_PATH / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    else:
        raise HTTPException(status_code=404, detail="Frontend not found")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)