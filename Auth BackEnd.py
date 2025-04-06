from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, static_folder='static')
app.secret_key = "your_secret_key"  # Secret key for session handling

@app.route("/app-details")
def app_details():
    category = request.args.get("category")
    index = int(request.args.get("index", 0))
    

    # Dummy apps data (replace with DB or shared structure if needed)
    apps = {
            "clean_drinking_water": [
                { "name": "💧 Jaldhoot App", 
                 "url": "appDetails.html?app=Jaldhoot", 
                 "description": "Jaldhoot App is a mobile application developed by the Indian government to monitor groundwater levels in rural areas. It enables officials to collect and record water level data from wells, aiding in sustainable water management and conservation efforts under the Jal Shakti Abhiyan. Jaldhoot App एक मोबाइल एप्लिकेशन है जिसे भारत सरकार द्वारा ग्रामीण क्षेत्रों में भूजल स्तर की निगरानी के लिए विकसित किया गया है। यह अधिकारियों को कुओं से जल स्तर डेटा एकत्र करने और रिकॉर्ड करने में सक्षम बनाता है, जिससे जल शक्ति अभियान के तहत सतत जल प्रबंधन और संरक्षण प्रयासों में सहायता मिलती है।"
                },
                { "name": "🚰 Jal Jeevan Mission", 
                 "url": "appDetails.html?app=JalJeevanMission", 
                 "description": "The Jal Jeevan Mission (JJM) App is an official government tool to track rural tap water supply under the Har Ghar Jal initiative. It provides real-time data on water connections, quality, and scheme progress, ensuring transparency and accountability. जल जीवन मिशन (JJM) ऐप एक सरकारी एप्लिकेशन है जो हर घर जल पहल के तहत ग्रामीण नल जल आपूर्ति को ट्रैक करता है। यह जल कनेक्शन, गुणवत्ता और योजना की प्रगति पर रीयल-टाइम डेटा प्रदान करता है, जिससे पारदर्शिता और जवाबदेही सुनिश्चित होती है।" 
                 }
            ],
            "agriculture": [
                { "name": "🛰 Kisan Suvidha", 
                 "url":  "appDetails.html?app=KisanSuvidha", 
                 "description": "An initiative by the Ministry of Agriculture, this app offers farmers real-time information on weather forecasts, market prices, plant protection, and expert advisories, aiding in informed decision-making. कृषि मंत्रालय की एक पहल, यह ऐप किसानों को मौसम पूर्वानुमान, बाजार मूल्य, पौध संरक्षण और विशेषज्ञ सलाह जैसी वास्तविक समय की जानकारी प्रदान करता है, जिससे वे सही निर्णय ले सकें।" 
                },
                { "name": "🤖 IFFCO Kisan", 
                 "url": "appDetails.html?app=IFFCOKisan", 
                 "description": "IFFCO Kisan is a digital platform that empowers farmers with agriculture advisory, weather updates, market prices, and advanced farming techniques. It provides real-time expert guidance to enhance productivity and profitability. इफको किसान एक डिजिटल प्लेटफॉर्म है जो किसानों को कृषि परामर्श, मौसम अपडेट, बाजार मूल्य और उन्नत खेती तकनीकों की जानकारी प्रदान करता है। यह उत्पादकता और लाभ बढ़ाने के लिए वास्तविक समय में विशेषज्ञ मार्गदर्शन उपलब्ध कराता है।" 
                },
                { "name": "📡 Plantix", 
                 "url": "appDetails.html?app=Plantix", 
                 "description": "Plantix is an AI-powered crop diagnosis app that helps farmers identify plant diseases, nutrient deficiencies, and pest infestations using just a smartphone camera. It provides personalized treatment suggestions and connects farmers with agricultural experts. प्लांटिक्स एक एआई-संचालित फसल निदान ऐप है जो किसानों को स्मार्टफोन कैमरे का उपयोग करके पौधों के रोग, पोषक तत्वों की कमी और कीट संक्रमण की पहचान करने में मदद करता है। यह व्यक्तिगत उपचार सुझाव देता है और किसानों को कृषि विशेषज्ञों से जोड़ता है।" 
                },
                { "name": "📊 Digital Green", 
                 "url": "appDetails.html?app=DigitalGreen", 
                 "description": "Digital Green is a technology-driven initiative that empowers small-scale farmers with community-led videos, AI-driven advisory, and data-driven insights to improve agricultural productivity and sustainability. डिजिटल ग्रीन एक तकनीक आधारित पहल है, जो छोटे किसानों को समुदाय-संचालित वीडियो, एआई-आधारित परामर्श और डेटा-समर्थित जानकारी प्रदान कर उनकी कृषि उत्पादकता और स्थिरता बढ़ाने में मदद करती है।" 
                }
            ],
            "women_empowerment": [
                { "name": "👩‍💼 eSARAS: Saras Aajeevika", 
                 "url": "appDetails.html?app=eSARAS", 
                 "description": "eSARAS, by the Ministry of Rural Development, is a digital platform that helps rural artisans and SHGs sell handmade products online, promoting women’s empowerment and sustainable livelihoods.ई-सारस, ग्रामीण विकास मंत्रालय का एक डिजिटल प्लेटफॉर्म है, जो ग्रामीण कारीगरों और SHGs को ऑनलाइन बिक्री में मदद करता है, जिससे महिला सशक्तिकरण और सतत आजीविका को बढ़ावा मिलता है।" 
                },

                { "name": "🚀 RUDI Sandesha Vyavhar (RSV)", 
                 "url": "appDetails.html?app=RUDI", 
                 "description": "RSV is a mobile-based rural distribution network that helps women entrepreneurs sell locally sourced agricultural products, ensuring fair trade and rural empowerment. आरएसवी एक मोबाइल-आधारित ग्रामीण वितरण नेटवर्क है, जो महिला उद्यमियों को स्थानीय कृषि उत्पाद बेचने में मदद करता है, जिससे न्यायसंगत व्यापार और ग्रामीण सशक्तिकरण को बढ़ावा मिलता है।" 
                 },
                { "name": "👩 GraamHaat", 
                 "url":"appDetails.html?app=GraamHaat" , 
                 "description": "GraamHaat is an agri-tech platform for livestock needs, powered by women SHG members from rural Rajasthan. It connects users with verified livestock farmer-preneurs in remote areas, ensuring direct access to quality livestock and services. ग्रामहाट एक एग्री-टेक प्लेटफॉर्म है, जो पशुधन सेवाओं के लिए ग्रामीण राजस्थान की महिला SHG सदस्यों द्वारा संचालित है। यह उपयोगकर्ताओं को प्रमाणित पशुपालकों से जोड़ता है, जिससे गुणवत्तापूर्ण पशुधन और सेवाएं सीधे मिलती हैं।"
                 }
            ],
            "education": [
                { "name": "📖 Google Bolo (Read Along)", 
                 "url": "appDetails.html?app=GoogleBolo", 
                 "description": "Google Bolo – Read Along App helps children improve reading skills through interactive stories and real-time feedback in multiple regional languages. Google Bolo – Read Along ऐप बच्चों को इंटरएक्टिव कहानियों और रीयल-टाइम फीडबैक के जरिए विभिन्न क्षेत्रीय भाषाओं में पढ़ने में मदद करता है।"
                },
                { "name": "🎓 eVidyaloka Learning App", 
                 "url": "appDetails.html?app=eVidyaloka", 
                 "description": "Provides educational content in regional languages for grades 5 to 8, featuring a child-friendly interface to enhance accessibility in rural areas. ​eVidyaloka लर्निंग ऐप कक्षा 5 से 8 के छात्रों के लिए क्षेत्रीय भाषाओं में उच्च-गुणवत्ता वाली डिजिटल शिक्षा प्रदान करता है। इसमें लाइव इंटरएक्टिव कक्षाएं, वीडियो पाठ और मूल्यांकन शामिल हैं, जिससे ग्रामीण क्षेत्रों के बच्चों के लिए सीखना सुलभ बनता है।" 
                 },
                { "name":"Educate Girls – PMS App", 
                 "url":"appDetails.html?app=EducateGirls", 
                 "description":"Educate Girls – PMS App aims to provide quality education for all under-served and marginalized girls by mobilizing and leveraging public, private, and community resources to improve access to education and school quality. यह ऐप लड़कियों की शिक्षा से जुड़ी पहल को बेहतर तरीके से प्रबंधित और ट्रैक करने में मदद करता है। इसकी मदद से टीम आसानी से डेटा जुटा सकती है, प्रगति पर नज़र रख सकती है और यह सुनिश्चित कर सकती है कि हर बच्ची को सही शिक्षा मिले।"
                 }
            ],
            "natural_resource_management": [
                { "name": "🌾 MRIDA (Soil Carbon Sequestration)", 
                 "url": "appDetails.html?app=MRIDA", 
                 "description": "Mrida is an initiative focused on sustainable rural development through agriculture, clean energy, and livelihood generation. It works with farmers, self-help groups, and rural communities to implement eco-friendly farming techniques, renewable energy solutions, and skill development programs to improve livelihoods while combating climate change. मृदा एक पहल है जो कृषि, स्वच्छ ऊर्जा और आजीविका सृजन के माध्यम से सतत ग्रामीण विकास पर केंद्रित है। यह किसानों, स्वयं सहायता समूहों और ग्रामीण समुदायों के साथ मिलकर पर्यावरण अनुकूल खेती, नवीकरणीय ऊर्जा समाधान और कौशल विकास कार्यक्रमों को लागू करता है, जिससे जीवन स्तर में सुधार हो और जलवायु परिवर्तन से निपटा जा सके।"
                },
                { "name": "🌱 India Observatory", 
                 "url": "appDetails.html?app=IndiaObservatory", 
                 "description": "India Observatory provides location-based data and analytics on natural resources to help rural communities manage them effectively. It offers data visualization tools for better planning and sustainable resource utilization.इंडिया ऑब्ज़र्वेटरी प्राकृतिक संसाधनों पर स्थान-विशिष्ट डेटा और विश्लेषण प्रदान करता है, जिससे ग्रामीण समुदाय उन्हें प्रभावी रूप से प्रबंधित कर सकें। यह बेहतर योजना और संसाधनों के सतत उपयोग के लिए डेटा विज़ुअलाइज़ेशन टूल्स प्रदान करता है।" 
                },
                { "name":"GIS Tools by Esri India", 
                 "url":"appDetails.html?app=GIS", 
                 "description":"Esri India's GIS tools help in mapping, spatial analysis, and resource management for sustainable development. These tools support better planning, optimize workflows, and mitigate environmental risks in rural and urban areas. एसरी इंडिया के जीआईएस टूल्स मानचित्रण, स्थानिक विश्लेषण और संसाधन प्रबंधन में मदद करते हैं, जिससे सतत विकास को बढ़ावा मिलता है। ये उपकरण बेहतर योजना, कार्यप्रवाह के अनुकूलन और पर्यावरणीय जोखिमों को कम करने में सहायक हैं।"
                }
            ],
            "healthcare": [
                { "name": "🚑 eSanjeevani", 
                 "url": "appDetails.html?app=eSanjeevani", 
                 "description": "A telemedicine service by the Indian government." 
                 },
                { "name": "🩺 Integrated Health Information Platform (IHIP)", 
                 "url": "appDetails.html?app=IHIP", 
                 "description": "An initiative by the Ministry of Health and Family Welfare, IHIP is a real-time, case-based surveillance system that enables the collection and analysis of health data across India. It aids in the early detection of disease outbreaks and efficient resource allocation. स्वास्थ्य और परिवार कल्याण मंत्रालय की एक पहल, IHIP एक रीयल-टाइम, केस-आधारित निगरानी प्रणाली है, जो भारत भर में स्वास्थ्य डेटा के संग्रह और विश्लेषण की सुविधा प्रदान करती है। यह बीमारी के प्रकोपों का शीघ्र पता लगाने और संसाधनों के प्रभावी आवंटन में सहायक है।" 
                 },
                { "name":"mSakhi",
                "url":"appDetails.html?app=mSakhi", 
                "description":"mSakhi is a mobile application designed to support community health workers (ASHAs - Accredited Social Health Activists) in providing maternal and child healthcare services in rural India. It offers interactive training, digital record-keeping, and real-time health tracking, helping improve healthcare access and reduce maternal and infant mortality rates."
                }
            ],
            "employment": [
                { "name": "💼 Mahila e-Haat", 
                "url": "appDetails.html?app=Mahila", 
                "description": "Mahila e-Haat, an initiative by the Ministry of Women and Child Development, is an online platform that empowers women entrepreneurs by providing them with a marketplace to showcase and sell their products. It supports women’s economic independence by connecting them directly with buyers across India. महिला एवं बाल विकास मंत्रालय की पहल, महिला ई-हाट एक ऑनलाइन प्लेटफॉर्म है जो महिला उद्यमियों को अपने उत्पादों को प्रदर्शित करने और बेचने का अवसर देता है। यह उन्हें आर्थिक रूप से सशक्त बनाता है और पूरे भारत में खरीदारों से जोड़ता है।" 
                },
                { "name": "💼  Udyam Sakhi", 
                 "url": "appDetails.html?app=Udyam", 
                 "description": "Udyam Sakhi, an initiative by the Ministry of Micro, Small & Medium Enterprises (MSME), is a digital platform that empowers women entrepreneurs by providing business resources, mentorship, financial assistance, and market linkages. It aims to support women in starting, growing, and sustaining their businesses. सूक्ष्म, लघु और मध्यम उद्यम मंत्रालय (MSME) की पहल, उद्योग सखी एक डिजिटल प्लेटफॉर्म है जो महिला उद्यमियों को व्यवसाय से जुड़े संसाधन, मार्गदर्शन, वित्तीय सहायता और बाजार से जोड़ने की सुविधा प्रदान करता है। इसका उद्देश्य महिलाओं को आत्मनिर्भर बनाना और उनके व्यवसाय को आगे बढ़ाने में सहायता करना है।" 
                }
            ],
            "climate":[
                { "name":"Farmonaut", 
                 "url":"appDetails.html?app=Farmanout", 
                 "description":"Farmonaut leverages satellite imagery to provide farmers with real-time data on crop health, soil conditions, and environmental changes. This enables precision farming, promotes resource efficiency, and supports sustainable agricultural practices. Farmonaut सैटेलाइट इमेजरी का उपयोग करके किसानों को उनकी फसल की सेहत, मिट्टी की स्थिति और पर्यावरणीय बदलावों की रीयल-टाइम जानकारी प्रदान करता है। यह सटीक खेती को बढ़ावा देता है, संसाधनों का कुशल उपयोग सुनिश्चित करता है और सतत कृषि को समर्थन देता है।"
                },
                { "name": "Soil Health Card", 
                 "url":"appDetails.html?app=SoilHealth", 
                 "description":"The Soil Health Card App helps farmers assess soil health by providing nutrient levels, pH balance, and fertilizer recommendations. It promotes sustainable farming, reduces fertilizer overuse, and helps combat climate change by preventing soil degradation and lowering greenhouse gas emissions.  सॉइल हेल्थ कार्ड ऐप किसानों को मिट्टी की जांच, पोषक तत्व स्तर और उर्वरक सिफारिशें प्रदान करता है। यह सतत खेती को बढ़ावा देता है, अत्यधिक उर्वरक उपयोग को कम करता है, और मिट्टी क्षरण रोककर व ग्रीनहाउस गैस उत्सर्जन घटाकर जलवायु परिवर्तन से लड़ने में मदद करता है।"
                 }
            ],
            "Goverment_Schemes":[
                { "description": "No recommendations to show at the moment"},
            ]
    
    }

    try:
        index = int(index)
        app_data = apps[category][index]
    except (KeyError, IndexError, ValueError):
        return "App not found.", 404
    lang = session.get('lang')
    if lang == 'hindi':
        return render_template('appDetails_hi.html', app=app_data)
    return render_template("appDetails.html", app=app_data)


# Initialize DB
def init_db():
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            email TEXT UNIQUE NOT NULL,
                            password TEXT NOT NULL)''')
        conn.commit()

init_db()
@app.route('/')
def splash():
    return render_template('splash.html')

@app.route('/auth')
def auth():
    return render_template('login.html')


# Login Page
@app.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")

    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()

    if user and check_password_hash(user[2], password):
        session["user"] = email
        return redirect(url_for("profiles_page"))
    return "Invalid credentials."

# Signup Page
@app.route("/signup", methods=["GET"])
def signup_page():
    
    return render_template("signup.html")

@app.route("/signup", methods=["POST"])
def signup():
    language = request.form.get("language")
    session['lang'] = language
    email = request.form.get("email")
    password = request.form.get("password")
    if not email or not password:
        return "Please enter both email and password."

    hashed_password = generate_password_hash(password)

    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, hashed_password))
            conn.commit()
        except sqlite3.IntegrityError:
            return "Email already exists."

    session["user"] = email
    return redirect(url_for("profiles_page"))


# Profiles Page
@app.route("/profiles")
def profiles_page():
    if "user" not in session:
        return redirect(url_for("login_page"))
    return render_template("profiles.html")
@app.route("/home")
def home_page():
    lang = session.get('lang')
    if lang == 'hindi':
        return render_template('home_hi.html')
    return render_template("home.html")
@app.route("/recommendations")
def recommendations_page():
    category = request.args.get("category", "general")
    lang = session.get('lang')
    if lang == 'hindi':
        return render_template('recommendations_hi.html', category=category)
    return render_template("recommendations.html", category=category)
'''@app.route("/app-details")
def app_details():
    category = request.args.get("category", "general")
    index = request.args.get("index")
    lang = session.get('lang')
    if lang == 'hindi':
        return render_template('appDetails_hi.html', category=category, index=index)
    return render_template("appDetails.html", category=category, index=index)
'''
@app.route("/download")
def download_page():
    app_name = request.args.get("app", "Unknown")
    lang = session.get('lang')
    if lang == 'hindi':
        return render_template('Download_hi.html', app_name=app_name)
    return render_template("Download.html", app_name=app_name)



# Logout
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login_page"))

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000
)
