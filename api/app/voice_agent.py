import json
import os

SCHEMES_PATH = "models/artifacts/schemes.json"

class VoiceAgent:
    def __init__(self):
        self.schemes = []
        self.load_schemes()
        
    def load_schemes(self):
        if os.path.exists(SCHEMES_PATH):
            with open(SCHEMES_PATH, 'r') as f:
                self.schemes = json.load(f)
            print(f"[INFO] Loaded {len(self.schemes)} schemes.")
        else:
            print("[WARN] schemes.json not found.")

    def find_schemes(self, query):
        """
        Simple keyword matching for 'Voice' queries.
        """
        query = query.lower()
        matches = []
        
        for scheme in self.schemes:
            # Check name or keywords
            if query in scheme['name'].lower():
                matches.append(scheme)
                continue
            
            for kw in scheme['keywords']:
                if kw in query:
                    matches.append(scheme)
                    break 
        
        if not matches:
             return [{
                 "name": "No direct match found",
                 "description": "Try keywords like 'loan', 'insurance', or 'soil'.",
                 "link": "#"
             }]
        
        return matches

voice_agent = VoiceAgent()
