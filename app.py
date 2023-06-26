from flask import Flask,render_template,request
import os
import cv2
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import zipfile
import shutil


def copy_files(source_folder, destination_folder):
    for root, dirs, files in os.walk(source_folder):
        for file in files:
            source_path = os.path.join(root, file)
            destination_path = os.path.join(destination_folder, file)
            shutil.copy(source_path, destination_path)

def zip_folder(folder_path, zip_path):
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, folder_path)
                zipf.write(file_path, arcname)
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("professional.html")
    # return render_template("profTest.html")

@app.route("/next",methods=["POST"])
def next():
    if(request.method == "POST"):
        f = os.listdir("static/design")

        for file in f:
            filepath = os.path.join("static/design", file)
            if os.path.isfile(filepath):
                os.unlink(filepath)
                print("file deleted Succesfully")

        f = os.listdir("static/web/design")

        for file in f:
            filepath = os.path.join("static/web/design", file)
            if os.path.isfile(filepath):
                os.unlink(filepath)
                print("file deleted Succesfully")
        a = request.form.to_dict()
        print(a)
        files = request.files
        print(files)
        imageExtension = []
        imageNames = []
        for i in files:
            if(i=='logo'):
                file = request.files[i]
                file.save("static/design/"+i+"."+file.filename.split(".")[-1])
                logoImage = "../design/"+i+"."+file.filename.split(".")[-1]
            elif(i=="background-selected"):
                file = request.files[i]
                file.save("static/design/"+i+"."+file.filename.split(".")[-1])
                bgimage = i+"."+file.filename.split(".")[-1]
                img = cv2.imread(f"static/design/{bgimage}")
                blurred = cv2.blur(img,(5,5))
                cv2.imshow("blure",blurred)
                cv2.imwrite("static/design/blurred_background.jpg", blurred)
                

            else:
                file = request.files[i]
                file.save("static/design/"+i+"."+file.filename.split(".")[-1])
                
                imageExtension.append(file.filename.split(".")[-1])
                imageNames.append(i)

        source_folder = 'static/design'
        destination_folder = 'static/web/design'
        copy_files(source_folder, destination_folder)

        print(imageExtension)
        # Style sheet for nav
        style = open("static/web/styleOutput.css","w")
        
        html = open("static/web/output.html",'w')
        html.write("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Document</title>
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" integrity="sha512-iecdLmaskl7CVkqkXNQ/ZH/XLlvWZOJyj7Yy7tcenmpD1ypASozpmT/E0iPtmFIB46ZmdtAc9eNBvH0H/ZpiBw==" crossorigin="anonymous" referrerpolicy="no-referrer" />
            <link rel="stylesheet" href="styleOutput.css">
            
        </head> """)

        html.write("""
        <script>
            function myfunc(){
                
                document.querySelector(".dropdown_menu").classList.toggle("open");
                console.log(document.querySelector(".dropdown_menu").classList.contains("open"));
                if(document.querySelector(".dropdown_menu").classList.contains("open")){
                    document.querySelector('.toggle_btn i').className = "fa-solid fa-xmark";
                    console.log(document.querySelector('.toggle_btn i').className);
                }
                else{
                    document.querySelector('.toggle_btn i').className = "fa-solid fa-bars";
                    console.log(document.querySelector('.toggle_btn i').className);

                }
                
            }
        </script>
        """)
        style.write("""
@import url('https://fonts.googleapis.com/css2?family=Raleway:wght@500&display=swap');

*{
    font-family: "Raleway",sans-serif;
}
        .logo img{
            height: 50px;
            padding: 5px;
        }
        html,body{
            margin:0;
            border:0;

        }
        li{
            list-style: none;
        }
        a{
            text-decoration: none;
            color: """+ a["nav-font-color"]+""";
            font-size: 1.1rem;
            padding: 8px;
            transition-duration: 0.2s;
            border-radius: 10px;
            font-weight: bold;
            padding: 10px;
            text-align: center;
            justify-content: center;
            
            
        }
        li a:hover{
            color: white;
            
            background-color: rgba(0, 0, 0, 0.1);
        
        }
        p{
            line-height:1.4rem;
        }

        /* Header */
        header{
            
            margin: 10px;
            background-color : """+ a["nav-bgcolor"]+""";
            
        }
        .navbar{
            
            flex-direction: row;
            height: 60px;
            max-width: 1500px;
            padding: 10px;
            display: flex;
            background-color:""" +  a["nav-bgcolor"] +
            """;
            /* margin-top: 8px; */
            align-items: center;
            justify-content: space-between;
            
            
            
        }
        .navbar .links{
            
            display: flex;
            gap: 1.5rem;
            flex-grow: 1;
            text-align: center;
            justify-content: right;
            


        }





        .navbar .toggle_btn{
            font-size: 1.5rem;
            cursor: pointer;
            background-color: transparent;
            border: none;
            display: none;
        }

        .action_btn{
            background-color: #fff;
            color: #0c0c0c;
            border-radius: 8px;
            outline: none;
            border: none;
            font-weight: bold;
            font-size: 0.7rem;
            cursor: pointer;
            transition-duration: 0.5s;
            
        }

        .action_btn:hover{
            transform: scale(1.1);
        }
        /* dropdown */
        .dropdown_menu{
            display: none;
            position: absolute;
            right: 2rem;
            height: 0;
            top: 60px;
            width: 300px;
            background: rgba(0, 0, 0, 0.2);
            backdrop-filter: blur(15px);
            border-radius: 10px;
            overflow: hidden;
            transition: height 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275) ;
        }
        .dropdown_menu.open{
            height:"""+str(int(a["nav-option-count"])*66)+"""px;
            z-index: 1;
        }

        .dropdown_menu li{
            padding: 0.7rem;
            display: flex;
            align-items: center;
            justify-content: center;
            background-color:transparent;
            color:"""+a["nav-font-color"]+""";
        }

        .dropdown_menu li:hover{
            background: rgba(0, 0, 0, 0.3);
            
        }
        .dropdown_menu li:hover a{
            color: #fff;
        }

        .dropdown_menu .action_btn{
            width: 100%;
            display: flex;
            justify-content: center;
        }
        .dropdown_menu .action_btn:hover{
            transform: scale(0.95);
        }
        .textarea{
            max-width:1200px;

            
        }
        .textarea *{
            padding :8px 15px;
        }
        .textarea p{
            text-indent : 40px;
        }

        @media(max-width:965px){
            .navbar .links,
            .navbar .action_btn{
                display: none;
            }
            .navbar .toggle_btn{
                display: block;
            }
            .dropdown_menu{
                display: block;
            }
            a{
                text-decoration: none;
                color: """+a["nav-font-color"]+""";
                font-size: 1.1rem;
                padding: 8px;
                transition-duration: 0.2s;
                border-radius: 10px;
                font-weight: bold;
                padding: 10px;
                text-align: center;
                background-color:"""+a["nav-bgcolor"]+""";
                justify-content: center;
                
                
                
            }
            li a:hover{
                color: rgb(22, 21, 21);
                
                background-color: transparent;
            
            }
        }
        @media(max-width:400px){
            .dropdown_menu{
                left: 2rem;
                width: unset;
            }
        }
        body{
                background-color:"""+a["background-color"]+""";
                color:"""+a["font-color"]+""";
            }

    
    
        """)
        # html.close()
        # style.close()
        # js.close()
        # ---------------------------------- NAVIGATION BAR ______________________________________________
        html = open("static/web/output.html","a+")
        style = open("static/web/styleOutput.css","a+")
        
        html.write("""  <body>
                   """)
        if(a["nav-select"] == "Style1"):
            html.write(f"""
        
            <header>
                <div class="navbar">
                    <div class="logo"><img src="{logoImage}" alt="" height="25px"></div>
                    <ul class="links">
            """)
            count = 1
            for i in range(int(a["nav-option-count"])):
                html.write(f"""
                <li><a href="{a[f"nav-option{count}"]}">{a[f"nav-option{count}"]}</a></li>
                """)
                count += 1
            html.write("""
            </ul>
            
                    <div>
                        <button class="toggle_btn" onclick="myfunc()"><i class="fa-solid fa-bars"></i></button>
                    </div>
                </div>
                <div class="dropdown_menu">
            
            
            """)
            count = 1
            for i in range(int(a["nav-option-count"])):
                html.write(f"""
                <li><a href="{a[f"nav-option{count}"]}">{a[f"nav-option{count}"]}</a></li>
                """)
                count += 1

            html.write("""
                    </div>
            </header>
            
            """)
        if(a["nav-select"] == "Style2"):
            
            html.write("""
        
            <header>
                <div class="navbar">
                    
                    <ul class="links">
            """)
            count = 1
            for i in range(int(a["nav-option-count"])):
                html.write(f"""
                <li><a href="{a[f"nav-option{count}"]}">{a[f"nav-option{count}"]}</a></li>
                """)
                count += 1
            html.write("""
            </ul>
            <div class="logo"><img src="..\design\logo.jpg" alt="" height="25px"></div>
                    <div>
                        <button class="toggle_btn" onclick="myfunc()"><i class="fa-solid fa-bars"></i></button>
                    </div>
                </div>
                <div class="dropdown_menu">
            
            
            """)
            count = 1
            for i in range(int(a["nav-option-count"])):
                html.write(f"""
                <li><a href="{a[f"nav-option{count}"]}">{a[f"nav-option{count}"]}</a></li>
                """)
                count += 1

            html.write(""""
                    </div>
            </header>
            
            """)



            style.write("""
                
            .navbar .links{
                
                
                justify-content: left;

            }
              
                
                """)
            # ------------------------------------NAVIGATION BAR END------------------------------------------
            # ------------------------------------Home Style -------------------------------------------------

        if(a["home-select"] == "Style1"):
                
            html.write(f"""
                
                <div class="home1">
        
                    <h1>{a["home-style1-oneliner"]}</h1>
                    <p>{a['home-style1-about']}</p>
                    
                    
                </div>
                """)
            style.write("""
                
                
                .home1{""")
            if(a["background-select-home"]=="color"):
                    style.write(f"""
                    background-color:{a["background-selected"]};
                    background-image:none;
                    """)
            elif(a["background-select-home"]=="image"):
                    try:
                        if(a["bgblur"] == "on"):
                            style.write("""
                            background-image: url('../design/blurred_background.jpg');
                            
                            """)
                    except(KeyError):
                        style.write(f"""
                        background-image: url('../design/{bgimage}');
                        """)
                    
                    style.write(f"""
                    background-size:cover;
                    background-repeat :none;
                    """)
            style.write("""

                    height: 90vh;
                    color: white;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    flex-direction: column;
                    
                    
                }
                .home1 h1{
                    font-size: 50px;
                    margin:20px;
                    text-align:center;
                
                }
                .home1 p{
                    max-width: 800px;
                    margin: 20px;
                    text-align:center;

                }
                
                """)
                

        elif(a["home-select"] == "Style2"):
            html.write(f"""
            
            <div class="home2or3">
                <img src="../design/home-style2-image.{imageExtension[imageNames.index("home-style2-image")]}">
                <div>
                    <h1>{a["home-style2-heading"]}</h1>
                    <p>{a["home-style2-about"]}</p>
                </div>
            </div>
            
            
            """)
        elif(a["home-select"] == "Style3"):
            html.write(f"""
            
            <div class="home2or3">
                
                <div>
                    <h1>{a["home-style3-heading"]}</h1>
                    <p>{a["home-style3-about"]}</p>
                </div>
                <img src="../design/home-style3-image.{imageExtension[imageNames.index("home-style3-image")]}">
            </div>
            
            
            """)
        if(a["home-select"] == "Style2" or a["home-select"] == "Style3"):
            style.write("""
            
            .home2or3{
            """)
            if(a["background-select-home"]=="color"):
                    style.write(f"""
                    background-color:{a["background-selected"]};
                    background-image:none;
                    """)
            elif(a["background-select-home"]=="image"):
                    try:
                        if(a["bgblur"] == "on"):
                            style.write("""
                            background-image: url('../design/blurred_background.jpg');
                            
                            """)
                    except(KeyError):
                        style.write(f"""
                        background-image: url('../design/{bgimage}');
                        """)
                    
                    style.write(f"""
                    background-size:cover;
                    background-repeat :none;
                    """)
            style.write("""
                display: flex;
                height: 90vh;
                flex-direction: row;
                justify-content: space-around;
                align-items: center;


            }
            .home2or3 *{
                padding: 20px;
            }
            .home2or3 h1{
                font-size:50px;
            }
            .home2or3 p{
                text-indent:50px;
                justify-content: center;
                align-items: center;
            }
            .home2or3 img{
                height: 450px;
    
}
             @media (max-width:650px) {
                
                .home2or3{
                    flex-direction: column;
                    justify-content:flex-start;
                    height:90vh;
                }
                .home2or3 *{
                text-align:center;
                margin:20px;
                }
                .home2or3 p{
                text-indent:50px;
                }
                .home2or3 h1{
                    margin:0;
                    padding:0;
                }
                .home2or3 img{
                height: 250px;

                }
                            }
                
            
            
            """)

        html.write("""
            
            <div class='blocks' id = 'blocks'>
              
            """)
        style.write("""
        
        .blocks{
            display:flex;
            flex-direction : row;
            flex-wrap:wrap;
            justify-content:space-around;
        }
        .blocks div{
            
            padding:10px;
        }
        .block3,.homeoption2,.homeoption1{
            display:flex;
            flex-basis : 100%;
            
        }
        .block3{
            align-items:center;
            justify-content:center;
        }
        .homeoption1{
            flex-direction:column;
            justify-content:center;
            align-items:center;
        }
        .homeoption1 h1{
            font-size:50px;
            margin:20px;
            text-align:center;
        }
        .homeoption1 p{
            max-width:800px;
            margin:20px;
            text-align:center;
        }
        .block3 img{
            height:250px;
            /* width:300px; */
            margin:40px;
            border-radius: 10px;
        }
        .block3{
            flex-wrap:wrap;
            margin:20px;
            justify-content:space-around;
        }
        .block1,.block2{
            display: flex;
            flex-direction: column;
            align-items: center;
            border-radius : 10px;
            margin:25px;
            justify-content:space-around;
            
        }
        
        .block1 p ,.block2 p{
            max-width: 500px;
            justify-content: center;
            text-indent:50px;
            

        }
        .block1 img ,.block2 img{
        height: 200px;
        width:auto;
        padding:15px;
        border-radius:10px;

        }
         @media (max-width:650px){
            .block3 img{
            height:200px;
            margin-top:20px;
            margin-bottom:20px;
        }
        .block3{
            margin:0px;
        }
         }
        """)
        block1 = 1
        block2 = 1
        block3 = 1
        home1 = 1
        home2 = 1
        home3 = 1
        
        extensionCount = 0
        contentOptions = []
        for i in range(int(a["totalBlock"])):
            contentOptions.append("content-option"+str(i))
        print(contentOptions)
        print(imageNames)

        for option in contentOptions:
            buttonCount = 0
            for key in a.keys():
                 if f"{option}-linkname" in key:
                      buttonCount+=1 
            print(buttonCount)
            if(a[option] == "Block1"):
                  html.write(f"""
                  
                    <div class='block1' style="background-color:{a[f"{option}-block1-bgcolor{block1}"]};color:{a[f"{option}-block1-fontcolor{block1}"]}">
                        <img src = '../design/{option}-block1-image{block1}.{imageExtension[imageNames.index(f"{option}-block1-image{block1}")]}'>
                        <p>{a[f"{option}-block1-text{block1}"]}</p>
                  """)
                  for i in range(1,buttonCount+1):
                        html.write(f"""
                        <a href='{a[f"{option}-link{i}"]}' >{a[f"{option}-linkname{i}"]}</a>
                        """)
                  html.write("""
                    </div>
                  """)
                  
                  block1 += 1

            if(a[option] == "Block2"):
                  html.write(f"""
                  
                    <div class='block2' style="background-color:{a[f"{option}-block2-bgcolor{block2}"]};color:{a[f"{option}-block2-fontcolor{block2}"]}" >
                        <p>{a[f"{option}-block2-text{block2}"]}</p>
                        <img src = '../design/{option}-block2-image{block2}.{imageExtension[imageNames.index(f"{option}-block2-image{block2}")]}'>
                    
                  
                  """)
                  for i in range(1,buttonCount+1):
                        html.write(f"""
                        <a href='{a[f"{option}-link{i}"]}' >{a[f"{option}-linkname{i}"]}</a>
                        """)
                  html.write("""
                    </div>
                  """)
                  block2 += 1
            if(a[option] == "Block3"):
                imageCount = 0
                for name in imageNames:
                    img = f"{option}-block3"
                    if(img in name):
                            imageCount += 1
                print(imageCount)   
                html.write(f"""
                
                    <div class='block3'>""")

                for i in range(1,imageCount+1):
                     html.write(f""" 
                     <img src='../design/{option}-block3-image{i}.{imageExtension[imageNames.index(f"{option}-block3-image{i}")]}'> 
                     """)

                for i in range(1,buttonCount+1):
                    html.write(f"""
                        <a href='{a[f"{option}-link{i}"]}' >{a[f"{option}-linkname{i}"]}</a>
                        """)
                html.write("""
                    </div>
                  """)
            if(a[option] == "Home1"):
                html.write(f"""
                    <div class= "homeoption1-{home1} homeoption1">
                        <h1>{a[f"{option}-home1-oneliner{home1}"]}</h1> 
                        <p>{a[f"{option}-home1-about{home1}"]}<p>
                    

                 """)
                for i in range(1,buttonCount+1):
                    html.write(f"""
                        <a href='{a[f"{option}-link{i}"]}' >{a[f"{option}-linkname{i}"]}</a>
                        """)
                html.write("""
                    </div>
                  """)
                style.write("""
                
                    .homeoption1-"""+str(home1)+"""{
                        background-image :url('../design/"""+f"{option}-home1-image{home1}.{imageExtension[imageNames.index(f'{option}-home1-image{home1}')]}"+"""');
                        height :100vh;
                        background-size:cover;
                        background-repeat:norepeat;
                    }
                
                """)
                home1 += 1
            if(a[option] == "Home2" or a[option] == "Home3"):
                 style.write("""
                 
                    
            .homeoption2{
                height: 100vh;
                display: flex;
                flex-direction: row;
                justify-content: space-evenly;
                align-items: center;
                margin:25px;

            }
            .homeoption2 *{
                padding: 25px;
            }
            .homeoption2 h1{
                font-size:50px;
            }
            .homeoption2 p{
                text-indent: 50px;
                justify-content: center;
                align-items: center;
            }
            .homeoption2 img{
                height: 450px;
    
            }
             @media (max-width:650px) {
                
                .homeoption2{
                    flex-direction: column;
                    justify-content:flex-start;
                    height:auto;
                }
                
                .homeoption2 *{
                text-align:center;
                
                }
                .homeoption2 p{
                text-indent:0px;
                }
                .homeoption2 h1{
                    margin:0;
                    padding:0;
                }
                .homeoption2 img{
                height: 180px;

                }
                .blocks a{
                    color: black;
                    background-color:white;
                    border-radius :7px;
                    border : 1px solid blac
                }
                            }

        
                 """)
            if(a[option] == "Home2"):
                html.write(f"""
                <div class="homeoption2"> 
                    <img src ='../design/{option}-home2-image{home2}.{imageExtension[imageNames.index(f"{option}-home2-image{home2}")]}'>
                    <div>
                        <h1>{a[f"{option}-home2-heading{home2}"]}</h1>
                        <p>{a[f"{option}-home2-about{home2}"]}</p>
                """)
                for i in range(1,buttonCount+1):
                    html.write(f"""
                        <a href='{a[f"{option}-link{i}"]}' >{a[f"{option}-linkname{i}"]}</a>
                        """)
                html.write("""
                    </div>
                
                 
                 """)
                
                html.write("""
                </div>
                  """)
                home2 += 1
            if(a[option] == "Home3"):
                html.write(f"""
                <div class="homeoption2"> 
                    
                    <div>
                        <h1>{a[f"{option}-home3-heading{home3}"]}</h1>
                        <p>{a[f"{option}-home3-about{home3}"]}</p>
                """)
                for i in range(1,buttonCount+1):
                    html.write(f"""
                        <a href='{a[f"{option}-link{i}"]}' >{a[f"{option}-linkname{i}"]}</a>
                        """)
                html.write(f"""
                    </div>
                    <img src ='../design/{option}-home3-image{home3}.{imageExtension[imageNames.index(f"{option}-home3-image{home3}")]}'>
                
                 
                 """)
                
                html.write("""
                    </div>
                  """)
                home3 += 1
            if(a[option] == "text-area"):
                count = 0
                html.write("""
                <div class = "textarea">
                
                """)
                for i in a.keys():
                     if(f"{option}-textarea-select" in i):
                        count +=1 
                count = int(count/2)
                for i in range(1,count+1):
                    if(a[f"{option}-textarea-select{i}"] == "heading"):
                        html.write(f"""
                        <h1>{a[f"{option}-textarea-select{i}-text"]}</h1>
                        """)
                    elif(a[f"{option}-textarea-select{i}"] == "subheading"):
                        html.write(f"""
                        <h3>{a[f"{option}-textarea-select{i}-text"]}</h3>
                        """)
                    elif(a[f"{option}-textarea-select{i}"] == "paragraph"):
                        html.write(f"""
                        <p>{a[f"{option}-textarea-select{i}-text"]}</p>
                        """)
                
                for i in range(1,buttonCount+1):
                       html.write(f"""
                       <a href='{a[f"{option}-link{i}"]}' >{a[f"{option}-linkname{i}"]}</a>
                       """)
                html.write("""
                </div>
                """)

        html.write("""
        </div>
        
        """)

        html.write("""
            
            </body>
</html>
            """)
        html.close()

    
    
    folder_to_zip = 'static/web/design'
    zip_file = 'static/images.zip'
    zip_folder(folder_to_zip, zip_file)


    return render_template("result.html")

@app.route("/sendEmail",methods=["POST"])
def send_email():
    if request.method == "POST":
        a = request.form.to_dict()
        print(a)
    


        mail_content = f'''
        Name :{a["name"]}
        E-Mail :{a["email"]}
        Feedback :{a["feedback"]}
        '''
        #The mail addresses and password
        sender_address = "ucode.udhay@gmail.com"
        sender_pass = "aglsxkjsmrbgsnmq"
        receiver_address = "udhaya4002@gmail.com"
        #Setup the MIME
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = receiver_address
        message['Subject'] = 'Feedback from User !'
        message.attach(MIMEText(mail_content))


        #Create SMTP session for sending the mail
        session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
        session.starttls() #enable security
        session.login(sender_address, sender_pass) #login with mail_id and password
        text = message.as_string()
        session.sendmail(sender_address, receiver_address, text)
        session.quit()
        print('Mail Sent')
    return "<script>alert('Thank You for your feedback !')</script>"

if __name__ ==  '__main__':
    app.run(debug=True)
