
import streamlit as st
from groq import Groq
import base64


st.set_page_config(
    page_title="NUTRIMIND AI",
    page_icon="🥗",
    layout="wide"
)


st.markdown("""
<style>
/* Main background */
.stApp {
    background-color: #0B1911;
    color: #F2F7F3;
}

/* Main content */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1250px;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #102418;
    border-right: 1px solid #244A33;
}

/* Sidebar text */
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label {
    color: #DCE9DF;
}

/* Headings */
h1, h2, h3 {
    color: #F2F7F3 !important;
}

/* Cards */
[data-testid="stMetric"],
div.st-key-card {
    background-color: #163020;
    border: 1px solid #244A33;
    border-radius: 14px;
    padding: 18px;
}

/* Buttons */
.stButton > button {
    background-color: #34D375;
    color: #0B1911;
    border: none;
    border-radius: 10px;
    font-weight: 600;
    padding: 10px 20px;
    transition: 0.2s;
}

.stButton > button:hover {
    background-color: #27B963;
    color: #0B1911;
    border: none;
}

/* Inputs */
.stTextInput input,
.stTextArea textarea,
.stSelectbox div[data-baseweb="select"] {
    background-color: #163020;
    border-color: #244A33;
    color: white;
}

/* Dividers */
hr {
    border-color: #244A33;
}

/* Footer */
.nutri-footer {
    background-color: #102418;
    border-top: 1px solid #244A33;
    padding: 22px;
    border-radius: 12px;
    margin-top: 55px;
    text-align: center;
}

.nutri-footer h4 {
    color: #34D375;
    margin-bottom: 7px;
}

.nutri-footer p {
    color: #A8BBAE;
    font-size: 13px;
    margin: 0;
}

/* Text areas */
.stTextArea textarea {
    background-color: #163020 !important;
    color: #F2F7F3 !important;
    border: 1px solid #244A33 !important;
    border-radius: 10px !important;
    -webkit-text-fill-color: #F2F7F3 !important;
}

/* Placeholder */
.stTextArea textarea::placeholder {
    color: #A8BBAE !important;
    -webkit-text-fill-color: #A8BBAE !important;
}

/* Focus */
.stTextArea textarea:focus {
    border: 1px solid #34D375 !important;
    box-shadow: 0 0 0 1px #34D375 !important;
}

/* Select boxes */
[data-baseweb="select"] > div {
    background-color: #163020 !important;
    border: 1px solid #244A33 !important;
    color: #F2F7F3 !important;
    border-radius: 10px !important;
}

/* Selected text */
[data-baseweb="select"] span {
    color: #F2F7F3 !important;
}

/* Dropdown menu */
[data-baseweb="popover"] {
    background-color: #163020 !important;
}

[data-baseweb="menu"] {
    background-color: #163020 !important;
}

/* Dropdown options */
[role="option"] {
    background-color: #163020 !important;
    color: #F2F7F3 !important;
}

[role="option"]:hover {
    background-color: #244A33 !important;
}

/* SIDEBAR DESIGN */
[data-testid="stSidebar"] {
    background: #102418 !important;
    border-right: 1px solid #244A33;
}

[data-testid="stSidebar"] > div:first-child {
    padding: 28px 16px;
}

/* Sidebar header */
.sidebar-brand {
    padding: 12px 10px 24px 10px;
    border-bottom: 1px solid #244A33;
    margin-bottom: 25px;
}

.sidebar-brand h2 {
    color: #34D375;
    font-size: 21px;
    margin: 0;
    letter-spacing: 1px;
}

.sidebar-brand p {
    color: #8DAA96;
    font-size: 10px;
    letter-spacing: 2px;
    margin: 5px 0 0 0;
}

/* Navigation title */
.sidebar-label {
    color: #789582;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 2px;
    padding: 0 10px;
    margin-bottom: 12px;
}

/* Navigation items */
[data-testid="stSidebar"] div[role="radiogroup"] {
    gap: 7px;
}

[data-testid="stSidebar"] div[role="radiogroup"] label {
    background: transparent;
    border-radius: 10px;
    padding: 11px 13px;
    transition: 0.2s;
    border: 1px solid transparent;
}

[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
    background: #163020;
    border-color: #244A33;
}

/* Selected navigation item */
[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {
    background: #163020;
    border: 1px solid #34D375;
}

[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) p {
    color: #34D375 !important;
    font-weight: 700;
}

/* Radio accent */
[data-testid="stSidebar"] input[type="radio"] {
    accent-color: #34D375;
}

/* Hide navigation label */
[data-testid="stSidebar"] div[data-testid="stWidgetLabel"] {
    display: none;
}

/* FILE UPLOADER */
[data-testid="stFileUploader"] section {
    background-color: #163020 !important;
    border: 1px dashed #34D375 !important;
    border-radius: 12px !important;
}

[data-testid="stFileUploader"] section > div {
    background-color: transparent !important;
}

[data-testid="stFileUploader"] button {
    background-color: #34D375 !important;
    color: #0B1911 !important;
    border: none !important;
}

[data-testid="stFileUploader"] small,
[data-testid="stFileUploader"] span,
[data-testid="stFileUploader"] label {
    color: #DCE9DF !important;
}

[data-testid="stFileUploader"] section:hover {
    border-color: #34D375 !important;
    background-color: #1B3A27 !important;
}

/* ALL SELECTBOXES */
[data-baseweb="select"] > div {
    background-color: #163020 !important;
    border: 1px solid #244A33 !important;
}

[data-baseweb="select"] input {
    color: #F2F7F3 !important;
}

[data-baseweb="select"] svg {
    fill: #34D375 !important;
}

[data-baseweb="popover"],
[data-baseweb="menu"] {
    background-color: #163020 !important;
}

[role="option"] {
    background-color: #163020 !important;
    color: #F2F7F3 !important;
}

[role="option"]:hover,
[aria-selected="true"] {
    background-color: #244A33 !important;
    color: #34D375 !important;
}

</style>
""", unsafe_allow_html=True)



# SIDEBAR BRAND
st.sidebar.markdown("""
<div class="sidebar-brand">
    <h2>NUTRIMIND AI</h2>
    <p>FOOD INTELLIGENCE</p>
</div>

<div class="sidebar-label">
    WORKSPACE
</div>
""", unsafe_allow_html=True)


# NAVIGATION
page = st.sidebar.radio(
    "Navigation",
    [
        "Home",
        "FoodVision",
        "RecipeMentor",
        "NutriScan",
        "FreshCheck",
        "FoodChat",
        "MealPlanner"
    ],
    label_visibility="collapsed"
)

# SIDEBAR FOOTER
st.sidebar.markdown("""
<div style="
    position: relative;
    margin-top: 45px;
    padding: 16px 10px;
    border-top: 1px solid #244A33;
">
    <p style="
        color:#34D375;
        font-size:12px;
        font-weight:600;
        margin:0;
    ">NUTRIMIND AI</p>

<p style="
    color:#789582;
    font-size:10px;
    margin-top:5px;
">Smart Food. Smarter Choices.</p>
</div>
""", unsafe_allow_html=True)



if page == "Home":

    st.title("NUTRIMIND AI")
    st.caption("Your intelligent food companion")

    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #17251d, #101a16, #17202a);
        padding: 38px;
        border-radius: 18px;
        border: 1px solid #34483b;
        margin: 15px 0 25px 0;
    ">
        <p style="color:#9fcea9; font-size:14px; letter-spacing:2px;">
            THE FUTURE OF SMART NUTRITION
        </p>
        <h1 style="color:white; font-size:38px; margin-bottom:12px;">
            Smart Food.<br>Smarter Choices.
        </h1>
        <p style="color:#d0d8d2; font-size:17px;">
            Discover what's on your plate, explore new recipes
            and make smarter food choices with AI.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Your AI-powered food platform")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("AI Modules", "06")

    with col2:
        st.metric("Food Assistance", "24/7")

    with col3:
        st.metric("Smart Platform", "AI Powered")

    st.divider()

    st.subheader("Explore our AI modules")
    st.write("Choose a tool and discover what NUTRIMIND can do.")

    modules = [
        ("FoodVision", "Identify food through images and camera."),
        ("RecipeMentor", "Create recipes using your ingredients."),
        ("NutriScan", "Discover nutritional information."),
        ("FreshCheck", "Explore visible signs of food freshness."),
        ("FoodChat", "Chat with your intelligent food assistant."),
        ("MealPlanner", "Generate personalized meal plans.")
    ]

    cols = st.columns(3)

    for i, (name, description) in enumerate(modules):

        with cols[i % 3]:

            st.markdown(f"""
            <div style="
                background:#171a1d;
                border:1px solid #30363b;
                border-radius:14px;
                padding:22px;
                min-height:155px;
                margin-bottom:15px;
            ">
                <h3 style="color:#a8d5b2; margin-bottom:12px;">
                    {name}
                </h3>
                <p style="color:#d0d0d0; font-size:14px;">
                    {description}
                </p>
            </div>
            """, unsafe_allow_html=True)

    st.divider()

    # st.markdown("""
    # <div style="text-align:center; padding:20px;">
    #     <h3 style="color:#a8d5b2;">Eat Smart. Live Smart.</h3>
    #     <p style="color:#999;">
    #         NUTRIMIND AI — Making food intelligence accessible to everyone.
    #     </p>
    # </div>
    # """, unsafe_allow_html=True)



elif page == "FoodVision":

    st.title("FoodVision")
    st.caption("AI-powered food recognition")
    st.divider()

    st.subheader("Discover what's on your plate")

    upload_tab, camera_tab = st.tabs(["Upload Image", "Take Photo"])

    with upload_tab:
        uploaded_image = st.file_uploader(
            "Upload a food image",
            type=["jpg", "jpeg", "png"],
            key="foodvision_file_upload"
        )

    with camera_tab:
        camera_image = st.camera_input(
            "Take a food photo",
            key="foodvision_camera"
        )

    if camera_image is not None:
        uploaded_image = camera_image

    if uploaded_image is not None:

        st.image(
            uploaded_image,
            caption="Your uploaded food",
            width=400
        )

        if st.button("Identify Food"):

            with st.spinner("FoodVision is analyzing your image..."):

                try:
                    image_bytes = uploaded_image.getvalue()

                    base64_image = base64.b64encode(
                        image_bytes
                    ).decode("utf-8")

                    mime_type = uploaded_image.type

                    groq_client = Groq(
                        api_key=st.secrets["GROQ_API_KEY"]
                    )

                    response = groq_client.chat.completions.create(
                        model="qwen/qwen3.8-27b",
                        messages=[
                            {
                                "role": "system",
                                "content": """
                                You are FoodVision, an AI food recognition assistant.
                                Identify foods carefully and explain what is visible.
                                Never invent ingredients that cannot be identified.
                                """
                            },
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "text",
                                        "text": """
                                        Analyze this food image.

                                        Include:
                                        1. Food name
                                        2. Visible ingredients
                                        3. Short description
                                        4. Possible cooking method
                                        5. General nutritional information

                                        If you are uncertain about the food,
                                        clearly mention that.
                                        """
                                    },
                                    {
                                        "type": "image_url",
                                        "image_url": {
                                            "url": f"data:{mime_type};base64,{base64_image}"
                                        }
                                    }
                                ]
                            }
                        ],
                        max_completion_tokens=1200,
                        temperature=0.4
                    )

                    result = response.choices[0].message.content
                    st.session_state.foodvision_result = result

                except Exception as e:
                    st.error(f"Food recognition failed: {e}")

    if "foodvision_result" in st.session_state:
        st.divider()
        st.subheader("FoodVision Analysis")
        st.markdown(st.session_state.foodvision_result)


elif page == "RecipeMentor":

    st.title("RecipeMentor")
    st.caption("Turn your ingredients into delicious recipes.")
    st.divider()

    st.subheader("What ingredients do you have?")

    ingredients = st.text_area(
        "Enter your ingredients",
        placeholder="Example: eggs, milk, flour, cheese, tomatoes..."
    )

    meal_type = st.selectbox(
        "Choose meal type",
        ["Any", "Breakfast", "Lunch", "Dinner", "Snack", "Dessert"]
    )

    difficulty = st.selectbox(
        "Cooking difficulty",
        ["Easy", "Medium", "Advanced"]
    )

    if st.button("Generate Recipe"):

        if not ingredients.strip():
            st.warning("Please enter at least one ingredient.")

        else:
            with st.spinner("RecipeMentor is creating your recipe..."):

                try:
                    groq_client = Groq(
                        api_key=st.secrets["GROQ_API_KEY"]
                    )

                    prompt = f"""
                    Create an original and practical recipe.

                    Available ingredients: {ingredients}
                    Meal type: {meal_type}
                    Difficulty: {difficulty}

                    Include:
                    1. Recipe name
                    2. Short description
                    3. Preparation time
                    4. Cooking time
                    5. Ingredients with quantities
                    6. Step-by-step instructions
                    7. Helpful cooking tips

                    Keep the instructions clear and easy to follow.
                    Mention any additional ingredients that are needed.
                    """

                    response = groq_client.chat.completions.create(
                        model="openai/gpt-oss-20b",
                        messages=[
                            {
                                "role": "system",
                                "content": "You are RecipeMentor, a creative and helpful cooking assistant."
                            },
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ],
                        max_tokens=1500,
                        temperature=0.7
                    )

                    recipe = response.choices[0].message.content

                    st.session_state.recipe_result = recipe

                except Exception as e:
                    st.error(f"Could not generate recipe: {e}")

    if "recipe_result" in st.session_state:
        st.divider()
        st.subheader("Your AI Recipe")
        st.markdown(st.session_state.recipe_result)

elif page == "NutriScan":

    st.title("NutriScan")
    st.caption("Explore the nutritional information of your food.")
    st.divider()

    st.subheader("Analyze your food")

    food = st.text_input(
        "Food name",
        placeholder="Example: Banana, rice, chicken..."
    )

    portion = st.number_input(
        "Portion size (grams)",
        min_value=1,
        max_value=2000,
        value=100
    )

    if st.button("Analyze Nutrition"):

        if not food.strip():
            st.warning("Please enter a food name.")

        else:
            with st.spinner("NutriScan is analyzing your food..."):

                try:
                    groq_client = Groq(
                        api_key=st.secrets["GROQ_API_KEY"]
                    )

                    prompt = f"""
                    Provide estimated nutritional information for:
                    Food: {food}
                    Portion: {portion} grams

                    Include:
                    - Calories (kcal)
                    - Protein (g)
                    - Carbohydrates (g)
                    - Fat (g)
                    - Fiber (g)
                    - Main vitamins and minerals

                    Also provide a short explanation of the nutritional
                    benefits of this food.

                    Use realistic approximate values.
                    Clearly state that values vary by preparation,
                    brand and ingredients.
                    Do not give medical advice.
                    """

                    response = groq_client.chat.completions.create(
                        model="openai/gpt-oss-20b",
                        messages=[
                            {
                                "role": "system",
                                "content": "You are NutriScan, an informative food nutrition assistant."
                            },
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ],
                        max_tokens=1200,
                        temperature=0.3
                    )

                    nutrition_result = response.choices[0].message.content

                    st.session_state.nutrition_result = nutrition_result

                except Exception as e:
                    st.error(f"Could not analyze food: {e}")

    if "nutrition_result" in st.session_state:
        st.divider()
        st.subheader("Nutrition Results")
        st.markdown(st.session_state.nutrition_result)



elif page == "FreshCheck":

    st.title("FreshCheck")
    st.caption("AI-powered visual freshness analysis")
    st.divider()

    st.subheader("Check your food")

    upload_tab, camera_tab = st.tabs(["Upload Image", "Take Photo"])

    with upload_tab:
        uploaded_image = st.file_uploader(
            "Upload a food image",
            type=["jpg", "jpeg", "png"],
            key="freshcheck_upload"
        )

    with camera_tab:
        camera_image = st.camera_input(
            "Take a food photo",
            key="freshcheck_camera"
        )

    if camera_image is not None:
        uploaded_image = camera_image

    if uploaded_image is not None:

        st.image(
            uploaded_image,
            caption="Uploaded food",
            width=400
        )

        if st.button("Analyze Freshness"):

            with st.spinner("FreshCheck is analyzing your food..."):

                try:
                    image_bytes = uploaded_image.getvalue()

                    base64_image = base64.b64encode(
                        image_bytes
                    ).decode("utf-8")

                    groq_client = Groq(
                        api_key=st.secrets["GROQ_API_KEY"]
                    )

                    response = groq_client.chat.completions.create(
                        model="qwen/qwen3.8-27b",
                        messages=[
                            {
                                "role": "system",
                                "content": """
                                You are FreshCheck, an AI visual food
                                freshness assistant.
                                Analyze only visible characteristics.
                                Never claim that food is definitely safe
                                or unsafe based only on an image.
                                """
                            },
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "text",
                                        "text": """
                                        Analyze this fruit or vegetable.

                                        Include:
                                        1. Identify the food.
                                        2. Describe its visible appearance.
                                        3. Look for visible discoloration,
                                           bruising, wrinkles or damage.
                                        4. Give a cautious visual assessment.
                                        5. Suggest appropriate storage advice.

                                        Use these assessment labels:
                                        - Appears fresh
                                        - Possible signs of aging
                                        - Visible signs of spoilage

                                        Explain your observations.

                                        Important: A photograph cannot
                                        determine whether food is safe
                                        to eat.
                                        """
                                    },
                                    {
                                        "type": "image_url",
                                        "image_url": {
                                            "url": f"data:{uploaded_image.type};base64,{base64_image}"
                                        }
                                    }
                                ]
                            }
                        ],
                        max_completion_tokens=1200,
                        temperature=0.4
                    )

                    result = response.choices[0].message.content
                    st.session_state.fresh_result = result

                except Exception as e:
                    st.error(f"Freshness analysis failed: {e}")

    if "fresh_result" in st.session_state:
        st.divider()
        st.subheader("FreshCheck Results")
        st.markdown(st.session_state.fresh_result)


elif page == "FoodChat":

    st.title("NUTRIMIND AI")
    st.caption("Your intelligent food assistant")

    st.markdown("""
<style>
/* Chat messages */
[data-testid="stChatMessage"] {
    background-color: #163020 !important;
    border: 1px solid #244A33 !important;
    border-radius: 14px !important;
    padding: 16px !important;
    margin-bottom: 12px;
}

/* Chat input container */
[data-testid="stChatInput"] {
    background-color: #163020 !important;
    border: 1px solid #244A33 !important;
    border-radius: 14px !important;
}

/* Chat input text */
[data-testid="stChatInput"] textarea {
    background-color: #163020 !important;
    color: #F2F7F3 !important;
    -webkit-text-fill-color: #F2F7F3 !important;
}

/* Chat placeholder */
[data-testid="stChatInput"] textarea::placeholder {
    color: #A8BBAE !important;
}
</style>
""", unsafe_allow_html=True)
    st.divider()

    if "food_chat_history" not in st.session_state:
        st.session_state.food_chat_history = []

    if not st.session_state.food_chat_history:
        st.markdown("## How can I help you today?")
        st.write("Ask me anything about food, recipes or nutrition.")

    for message in st.session_state.food_chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    question = st.chat_input("Ask NUTRIMIND anything...")

    if question:

        st.session_state.food_chat_history.append({
            "role": "user",
            "content": question
        })

        with st.chat_message("user"):
            st.markdown(question)

        with st.spinner("NUTRIMIND is thinking..."):

            try:
                history = st.session_state.food_chat_history[:-1]

                prompt = """
                You are NUTRIMIND AI, a helpful food assistant.
                Answer clearly about food, recipes and general nutrition.
                Do not provide medical diagnoses or extreme dieting advice.
                """

                groq_client = Groq(
                    api_key=st.secrets["GROQ_API_KEY"]
                )

                messages = [
                    {"role": "system", "content": prompt}
                ]

                messages.extend(history)

                messages.append({
                    "role": "user",
                    "content": question
                })

                response = groq_client.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    messages=messages,
                    max_tokens=3000,
                    temperature=0.6
                )

                answer = response.choices[0].message.content

            except Exception as e:
                answer = "AI is temporarily unavailable. Please try again."
                st.error(str(e))

        with st.chat_message("assistant"):
            st.markdown(answer)

        st.session_state.food_chat_history.append({
            "role": "assistant",
            "content": answer
        })


elif page == "MealPlanner":

    st.title("MealPlanner")
    st.caption("Your personal AI meal planner")
    st.divider()

    st.subheader("Create your meal plan")

    goal = st.selectbox(
        "What kind of meal plan do you want?",
        [
            "Balanced everyday meals",
            "Vegetarian meals",
            "Quick and easy meals",
            "Budget-friendly meals"
        ]
    )

    preferences = st.text_area(
        "Food preferences or allergies",
        placeholder="Example: I like pasta, rice and vegetables..."
    )

    days = st.selectbox(
        "Choose duration",
        ["1 day", "3 days", "5 days", "7 days"]
    )

    if st.button("Generate Meal Plan"):

        with st.spinner("Creating your meal plan..."):

            try:
                groq_client = Groq(
                    api_key=st.secrets["GROQ_API_KEY"]
                )

                prompt = f"""
Create a complete meal plan for {days}.

Type: {goal}
Preferences: {preferences}

IMPORTANT:
- Include EVERY requested day.
- Clearly label them Day 1, Day 2, Day 3, etc.
- Include breakfast, lunch and dinner for EACH day.
- Give different meals for every day.
- Keep descriptions short and clear.
- Never stop after Day 1.
- Use balanced meals and ordinary ingredients.
- Do not include calorie restrictions.
"""
              

                response = groq_client.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are NUTRIMIND AI, a helpful meal planning assistant."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    max_tokens=1500,
                    temperature=0.6
                )

                meal_plan = response.choices[0].message.content

                st.session_state.meal_plan = meal_plan

            except Exception as e:
                st.error(f"Could not generate meal plan: {e}")

    if "meal_plan" in st.session_state:
        st.divider()
        st.subheader("Your AI Meal Plan")
        st.markdown(st.session_state.meal_plan)


# # GLOBAL FOOTER
# st.markdown("""
# <div class="nutri-footer">
#     <h4>NUTRIMIND AI</h4>
#     <p>Smart Food. Smarter Choices.</p>
#     <p style="margin-top:10px;">
#         AI-powered food intelligence
#     </p>
#     <p style="margin-top:10px;">
#         © 2026 NUTRIMIND AI. All rights reserved.
#     </p>
# </div>
# """, unsafe_allow_html=True)
