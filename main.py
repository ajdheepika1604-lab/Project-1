import streamlit as st
import mysql.connector
import pandas as pd
import traceback

# Set page config
st.set_page_config(page_title='Cricbuzz LiveStats', layout='wide')

# Database connection function
def get_connection():
    return mysql.connector.connect(
        host="localhost",          # Replace with your host
        user="root",          # Replace with your username
        password="Dheepika@123",  # Replace with your password
        database="cricbuzz_db"   # Replace with your database name
    )

# Sidebar navigation pages
pages = [
    "🏠 Home",
    "🏏 Live Match",
    "📊 Top Player Stats",
    "💻 SQL Practice",
    "📝 CRUD Operations"
]
page = st.sidebar.selectbox("Navigate", pages)

if page == "🏠 Home":
    st.title("Welcome All! 🏏📚")
    st.markdown("""
    Welcome to the **Cricbuzz LiveStats Dashboard** — your go-to platform to bring cricket analytics seamlessly into the classroom.  
    Explore player stats, live matches, and interactive SQL practice designed for educators. Let's make learning cricket fun and insightful!
    """)
    col1, col2, col3 = st.columns(3)
    col1.metric("Upcoming Matches", "5", "2 starting today")
    col2.metric("Top Players", "10+", "Updated weekly")
    col3.metric("SQL Practice Problems", "13", "New problems every month")
    st.image(r"C:\Users\Dheepika Aj\Downloads\VS code\env\Cricket image.jpg", caption="Engage your students with cricket analytics!")

elif page == "🏏 Live Match":
    st.subheader("Live Match Updates 🏏")
    try:
        conn = get_connection()
        query = """
            SELECT series_id, series_name, match_id, match_desc, match_format, team1, team2, venue, status
            FROM live_match;
        """
        df = pd.read_sql_query(query, conn)
        conn.close()
        if not df.empty:
            st.table(df)
        else:
            st.info("No live matches in the database.")
    except Exception as e:
        st.error("Error loading live matches:")
        st.error(str(e))
        st.text(traceback.format_exc())

elif page == "📊 Top Player Stats":
    st.title("🏏 Player Profile Viewer")

    def fetch_players():
        conn = get_connection()
        df = pd.read_sql("SELECT id, name FROM player_profiles", conn)
        conn.close()
        return df

    def fetch_player_details(player_id):
        conn = get_connection()
        query = "SELECT * FROM player_profiles WHERE id = %s"
        df = pd.read_sql(query, conn, params=(player_id,))
        conn.close()
        if not df.empty:
            return df.iloc[0]
        return None

    try:
        players_df = fetch_players()
        player_options = players_df.set_index("id")["name"].to_dict()
        selected_name = st.selectbox("Select a player", options=list(player_options.values()))
        # Get player id by name
        selected_id = next(key for key, value in player_options.items() if value == selected_name)
        player = fetch_player_details(selected_id)

        if player is not None:
            header_col, image_col = st.columns([3, 1])
            with header_col:
                st.markdown(f"## {player['name']}  ({player['nickName']})")
            with image_col:
                st.image(player['image'], width=180)
            st.markdown("---")

            left_col, middle_col, right_col = st.columns(3)
            with left_col:
                st.subheader("🏏 Cricket Info")
                st.markdown(f"**Role:** {player['role']}")
                st.markdown(f"**Batting Style:** {player['bat']}")
                st.markdown(f"**Bowling Style:** {player['bowl']}")
            with middle_col:
                st.subheader("📋 Personal Details")
                st.markdown(f"**Height:** {player['height']}")
                st.markdown(f"**Birth Place:** {player['birthPlace']}")
                st.markdown(f"**Date of Birth:** {player['DoB']}")
            with right_col:
                st.subheader("🌍 Teams & Country")
                st.markdown(f"**International Team:** {player['intlTeam']}")
                with st.expander("Teams Played For"):
                    teams_list = player['teams'].split(", ")
                    for team in teams_list:
                        st.write(f"- {team}")
            st.markdown("---")
            with st.expander("📖 Biography"):
                st.write(player['bio'])
        else:
            st.warning("Player details not found. Please select another player.")
    except Exception as e:
        st.error("Error loading player data:")
        st.error(str(e))
        st.text(traceback.format_exc())

elif page == "💻 SQL Practice":
    st.title("SQL Practice Questions")

    def run_query(query):
        conn = get_connection()
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df

    queries = {
        "Find all players who represent India.": """
            SELECT player_name, team_name FROM trending WHERE team_name = 'India';
        """,
        "Find all all-rounder players.": """
            SELECT player_id, name, role, batting_style, bowling_style, player_type FROM players_info WHERE player_type = 'ALL ROUNDERS';
        """,
        "Find all wicket keeper players.": """
            SELECT player_id, name, role, batting_style, bowling_style, player_type FROM players_info WHERE player_type = 'WICKET KEEPERS';
        """,
        "Find all batter players.": """
            SELECT player_id, name, role, batting_style, bowling_style, player_type FROM players_info WHERE player_type = 'BATTERS';
        """,
        "Find all ODI matches.": """
            SELECT match_id, series_id, series_name, match_desc, match_format, status, team1, team2, venue, city FROM venue_matches WHERE match_format = 'ODI';
        """,
        "Find venues with a capacity of 11,600.": """
            SELECT venue_id, name, city, country, timezone, capacity, ends, home_team FROM venues_info WHERE capacity = '11,600';
        """,
        "Find the highest individual score in each format.": """
            SELECT b.innings_id AS format, b.batsman_id, b.name, b.balls, b.runs AS highest_score, b.fours, b.sixes, b.strkrate
            FROM batsman_scorecard b
            INNER JOIN (
                SELECT innings_id, MAX(runs) AS max_runs FROM batsman_scorecard GROUP BY innings_id
            ) sub ON b.innings_id = sub.innings_id AND b.runs = sub.max_runs;
        """,
        "Find all players who bat right-handed.": """
            SELECT player_id, name, role, batting_style, bowling_style, player_type FROM players_info WHERE batting_style = 'Right-hand bat';
        """,
        "Find all players who bat left-handed.": """
            SELECT player_id, name, role, batting_style, bowling_style, player_type FROM players_info WHERE batting_style = 'Left-hand bat';
        """,
        "Find all batsmen with a strike rate above 100.": """
            SELECT batsman_id, name, balls, strkrate FROM batsman_scorecard WHERE strkrate > 100;
        """,
        "Find all TEST matches.": """
            SELECT match_id, series_id, series_name, match_desc, match_format, status, team1, team2, venue, city FROM venue_matches WHERE match_format = 'TEST';
        """,
        "Find all T20 matches.": """
            SELECT match_id, series_id, series_name, match_desc, match_format, status, team1, team2, venue, city FROM venue_matches WHERE match_format = 'T20';
        """,
        "Find top 15 players based on their rank.": """
            SELECT player_id, player_name, player_rank, country, rating FROM stats_rank WHERE player_rank BETWEEN 1 AND 15 ORDER BY player_rank ASC;
        """
    }

    question = st.selectbox("Choose a question", list(queries.keys()))
    if st.button("Run Query"):
        try:
            result_df = run_query(queries[question])
            st.dataframe(result_df)
        except Exception as e:
            st.error("Error running query:")
            st.error(str(e))
            st.text(traceback.format_exc())
elif page == "📝 CRUD Operations":
    st.title("🛠️ CRUD Operations")
    st.markdown("## 📝 **Create, Read, Update, Delete Player Records**")

    operation = st.selectbox(
        "Choose an operation:",
        ['Add (New Player)', 'Update (Edit Player)', 'Delete (Remove Player)', 'View (All Players)'],
        index=0
    )

    st.markdown("---")

    if operation == 'Add (New Player)':
        with st.expander("➕ Add New Player", expanded=True):
            with st.form("add_player_form"):
                col1, col2 = st.columns(2)
                name = col1.text_input("Name")
                role = col2.text_input("Role")
                is_captain = col1.selectbox("Is Captain?", ["0", "1"])  # 0 = No, 1 = Yes
                batting_style = col2.text_input("Batting Style")
                bowling_style = col1.text_input("Bowling Style")
                player_type = col2.text_input("Player Type")
                submit = st.form_submit_button("Add Player")

                if submit:
                    if not all([name, role, is_captain, batting_style, bowling_style, player_type]):
                        st.warning("Please fill in all fields before submitting.")
                    else:
                        try:
                            conn = get_connection()
                            cursor = conn.cursor()

                            # Get max player_id and manually increment (if no AUTO_INCREMENT)
                            cursor.execute("SELECT MAX(player_id) FROM player")
                            max_id = cursor.fetchone()[0]
                            next_id = 1 if max_id is None else max_id + 1

                            cursor.execute(
                                "INSERT INTO player (player_id, name, role, is_captain, batting_style, bowling_style, player_type) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                                (next_id, name, role, is_captain, batting_style, bowling_style, player_type)
                            )
                            conn.commit()
                            cursor.close()
                            conn.close()
                            st.success(f"✅ Player '{name}' added successfully with player_id {next_id}.")
                        except Exception as e:
                            st.error("❌ Error adding player:")
                            st.error(str(e))


    elif operation == 'Update (Edit Player)':
        with st.expander("✏️ Update Player Information", expanded=True):
            player_name = st.text_input("Search player to update:")
            if player_name:
                conn = get_connection()
                df = pd.read_sql("SELECT * FROM player WHERE name LIKE %s", conn, params=(f"%{player_name}%",))
                conn.close()
                if not df.empty:
                    player = df.iloc[0]
                    with st.form("update_player_form"):
                        name_new = st.text_input("Name", value=player['name'])
                        role_new = st.text_input("Role", value=player['role'])
                        is_captain_new = st.selectbox("Is Captain?", ["0", "1"], index=int(player['is_captain']))
                        batting_style_new = st.text_input("Batting Style", value=player['batting_style'])
                        bowling_style_new = st.text_input("Bowling Style", value=player['bowling_style'])
                        player_type_new = st.text_input("Player Type", value=player['player_type'])
                        submit_update = st.form_submit_button("Update Player")
                        if submit_update:
                            try:
                                conn = get_connection()
                                cursor = conn.cursor()
                                cursor.execute(
                                    "UPDATE player SET name=%s, role=%s, is_captain=%s, batting_style=%s, bowling_style=%s, player_type=%s WHERE player_id=%s",
                                    (name_new, role_new, is_captain_new, batting_style_new, bowling_style_new, player_type_new, int(player['player_id']))
                                )
                                conn.commit()
                                cursor.close()
                                conn.close()
                                st.success(f"✅ Player '{name_new}' updated successfully.")
                            except Exception as e:
                                st.error("❌ Error updating player:")
                                st.error(str(e))
                else:
                    st.warning("No player found with that name.")


    elif operation == 'Delete (Remove Player)':
        with st.expander("🗑️ Delete Player", expanded=True):
            player_name_del = st.text_input("Search player to delete:")
            if player_name_del:
                conn = get_connection()
                df = pd.read_sql("SELECT * FROM player WHERE name LIKE %s", conn, params=(f"%{player_name_del}%",))
                conn.close()
                if not df.empty:
                    player = df.iloc[0]
                    if st.button(f"Delete {player['name']}"):
                        try:
                            conn = get_connection()
                            cursor = conn.cursor()
                            cursor.execute("DELETE FROM player WHERE player_id=%s", (int(player['player_id']),))
                            conn.commit()
                            cursor.close()
                            conn.close()
                            st.success(f"✅ Player '{player['name']}' deleted.")
                        except Exception as e:
                            st.error("❌ Error deleting player:")
                            st.error(str(e))
                else:
                    st.warning("No player found with that name.")


    elif operation == 'View (All Players)':
        with st.expander("📋 View All Players", expanded=True):
            conn = get_connection()
            df = pd.read_sql("SELECT * FROM player", conn)
            conn.close()
            st.dataframe(df)

    st.markdown("---")
    st.markdown("### 📈 **Quick Database Statistics**")
    if st.button("Show Current Stats"):
        conn = get_connection()
        total_players = pd.read_sql("SELECT COUNT(*) as count FROM player", conn).iloc[0]['count']
        conn.close()
        st.info(f"Total Players: {total_players}")
