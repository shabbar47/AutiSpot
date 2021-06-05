from flask import render_template, request, redirect, url_for, session, flash, jsonify
from model import *
from datetime import datetime
import os
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'