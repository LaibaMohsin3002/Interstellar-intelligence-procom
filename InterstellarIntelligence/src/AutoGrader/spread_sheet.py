import os
import gspread
from google.oauth2.service_account import Credentials

FILE_DIR = os.path.dirname(os.path.abspath(__file__))

def setup_sheet():
    """
    Sets up the Google Sheets client and opens the spreadsheet by its ID.
    
    Returns:
        gspread.models.Spreadsheet: The opened spreadsheet object.
    """
    
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
    ]

    creds_file = os.path.join(FILE_DIR, "credentials.json")
    creds = Credentials.from_service_account_file(creds_file, scopes=scopes)
    client = gspread.authorize(creds)

    sheet_id = "1C3E7gEnyUQwTTpEzA8L88rmP0CB-ktPkEJTNc3F7Uds"
    sheet = client.open_by_key(sheet_id)
    return sheet

class SpreadSheet:
    def __init__(self):
        self.sheet = setup_sheet()

    def add_score(self, team_name, score):
        """
        Adds or updates the score for a given team in the spreadsheet.
        If the team name does not exist in the first column of the worksheet,
        it appends a new row with the team name and score. If the team name
        already exists, it updates the score in the corresponding row.
        Args:
            team_name (str): The name of the team.
            score (int or float): The score to be added or updated.
        Returns:
            None
        """
        worksheet = self.sheet.get_worksheet(0)
        team_names = worksheet.col_values(1)[1:]
        
        if team_name not in team_names:
            worksheet.append_row([team_name, score])
        else:
            team_index = team_names.index(team_name) + 2
            worksheet.update_cell(team_index, 2, score)            

    def get_scores(self):
        """
        Retrieves scores from the second column of the first worksheet.
        This method accesses the first worksheet of the spreadsheet and retrieves
        all values from the second column, excluding the header. It then converts
        these values to floats and returns them as a list.
        Returns:
            list of float: A list of scores as floating-point numbers.
        """
        
        worksheet = self.sheet.get_worksheet(0)
        scores_list = worksheet.col_values(2)[1:]
        scores = [float(score) for score in scores_list]
        return scores

    def get_team_score(self, team_name):
        """
        Retrieves the score for a given team from the spreadsheet.
        Args:
            team_name (str): The name of the team whose score is to be retrieved.
        Returns:
            float: The score of the specified team.
        Raises:
            ValueError: If the team name is not found in the spreadsheet.
        """
        
        worksheet = self.sheet.get_worksheet(0)
        team_names = worksheet.col_values(1)[1:]
        team_index = team_names.index(team_name) + 2
        score = worksheet.cell(team_index, 2).value
        return float(score)