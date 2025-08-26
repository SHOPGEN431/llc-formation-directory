from app import app

# This is the entry point for Vercel
# The app variable must be available at module level for Vercel to find it
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
