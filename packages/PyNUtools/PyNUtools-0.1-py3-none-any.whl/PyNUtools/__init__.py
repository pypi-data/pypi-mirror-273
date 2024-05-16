def Mothers_day_coder(how_your_call_your_mother, how_you_are_called_by_your_mother, custom_title, general_message_T_or_F, custom_message=None):
   html_code = """"""

   if general_message_T_or_F == False:
      html_code = f'''<!DOCTYPE html>
      <html lang="en">
      <head>
          <meta charset="UTF-8">
          <meta name="viewport" content="width=device-width, initial-scale=1.0">
          <title>{custom_title}</title>
          <link rel="stylesheet" href="styles.css">
      </head>
      <body><div class="container">
          <div class="balloon"></div>
          <div class="balloon"></div>
          <div class="balloon"></div>
          <div class="balloon"></div>
          <div class="balloon"></div>
      
          <div class="card">
              <h1>Happy Mother's Day {how_your_call_your_mother} :-)</h1>
              <p>Dear {how_your_call_your_mother}, {custom_message}</p>
              <p id="message">With love,</p>
              <p>{how_you_are_called_by_your_mother}</p>
          </div>
      </div>
      </body>
      </html>
      '''

   elif general_message_T_or_F == True:
      html_code = f'''<!DOCTYPE html>
      <html lang="en">
      <head>
          <meta charset="UTF-8">
          <meta name="viewport" content="width=device-width, initial-scale=1.0">
          <title>{custom_title}</title>
          <link rel="stylesheet" href="styles.css">
      </head>
      
      <body><div class="container">
          <div class="balloon"></div>
          <div class="balloon"></div>
          <div class="balloon"></div>
          <div class="balloon"></div>
          <div class="balloon"></div>

          <div class="card">
              <h1>Happy Mother's Day {how_your_call_your_mother} 🤱</h1>
              <p>Dear {how_your_call_your_mother},
              Happy Mother's Day! Your love and guidance have shaped me into who I am today. Thank you for being my rock, my confidant, and my biggest cheerleader. Today and every day, I celebrate you and the beautiful bond we share. I love you more than words can say.</p>
              <p id="message">With love,</p>
              <p>{how_you_are_called_by_your_mother}</p>
          </div>
      </div>
      </body>
      </html>
      '''
   else:
      exit(43)

   css_code = """body {
          margin: 0;
          padding: 0;
          background: hsl(70, 31%, 85%);
          text-align: center;
          overflow: hidden;
          display: flex;
          justify-content: center;
          align-items: center;
          height: 100vh;
      }
      
      .container {
          position: relative;
      }
      
      .balloon {
          width: 120px;
          height: 145px;
          background: hsl(215, 50%, 65%);
          border-radius: 80%;
          position: absolute;
          box-shadow: inset -10px -10px 0 rgba(0, 0, 0, 0.07);
          transition: transform 0.5s ease;
          z-index: 0;
          transform-origin: bottom center;
      }
      
      @keyframes balloons {
          0%, 100% { transform: translateY(0) rotate(-4deg); }
          50% { transform: translateY(-25px) rotate(4deg); }
      }
      
      .balloon:before {
          content: "▲";
          font-size: 20px;
          color: hsl(215, 30%, 50%);
          display: block;
          text-align: center;
          width: 100%;
          position: absolute;
          bottom: -12px;
          z-index: -100;
      }
      
      .balloon:after {
          content: "";
          display: inline-block;
          position: absolute;
          top: 153px;
          left: 50%;
          height: 250px;
          width: 1px;
          margin: 0 auto;
          background: rgba(0, 0, 0, 0.2);
      }
      
      .balloon:nth-child(2) { background: hsl(245, 40%, 65%); animation-duration: 3.5s; }
      .balloon:nth-child(2):before { color: hsl(245, 40%, 65%); }
      
      .balloon:nth-child(3) { background: hsl(139, 50%, 60%); animation-duration: 3s; }
      .balloon:nth-child(3):before { color: hsl(139, 30%, 50%); }
      
      .balloon:nth-child(4) { background: hsl(59, 50%, 58%); animation-duration: 4.5s; }
      .balloon:nth-child(4):before { color: hsl(59, 30%, 52%); }
      
      .balloon:nth-child(5) { background: hsl(23, 55%, 57%); animation-duration: 5s; }
      .balloon:nth-child(5):before { color: hsl(23, 44%, 46%); }
      
      .card {
          background-color: #fff;
          padding: 80px;
          border-radius: 50%;
          box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
          max-width: 600px;
          margin: 0 auto;
          overflow: hidden;
          position: relative;
          transition: transform 1s ease;
          z-index: 1; 
      }
      
      .card:hover { transform: scale(0.95); }
      
      h1 {
          display: block;
          opacity: 1;
          color: #ff6f61;
          margin-bottom: 20px;
          font-size: 80px;
          transition: font-size 1s ease;
      }
      
      .card:hover h1 {
          display: none;
          opacity: 0;
          transition: opacity 0.3s ease;
      }
      
      p { display: none; }
      
      .card:hover p {
          display: block;
          opacity: 1;
          font-size: 40px;
          transition: opacity 1s ease;
      }
      
      #message {
          font-size: 40px;
          transition: font-size 1s ease;
      }
      
      #message::first-letter {
          font-size: 150%;
          font-weight: bold;
      }
      
      .balloon:nth-child(1) { left: 10%; bottom: -20%; }
      .balloon:nth-child(2) { left: 30%; bottom: -20%; }
      .balloon:nth-child(3) { left: 50%; bottom: -20%; }
      .balloon:nth-child(4) { left: 70%; bottom: -20%; }
      .balloon:nth-child(5) { left: 90%; bottom: -20%; }
      
      .balloon {
          animation: balloons 4s ease-in-out infinite, move-up 10s linear infinite; /* Add the move-up animation */
      }
      
      @keyframes move-up {
          0% { top: 100%; }
          100% { top: -20%; }
      }
      """

   js_code = """document.addEventListener("DOMContentLoaded", function() {
          const message = document.getElementById("message");
      
          message.style.opacity = 0;
          setTimeout(() => {
              message.style.transition = "opacity 0.5s";
              message.style.opacity = 1;
          }, 500);
      
          setInterval(() => {
              const randomColor = getRandomColor();
              message.style.transition = "color 0.5s";
              message.style.color = randomColor;
          }, 5000);
      
          function getRandomColor() {
              const letters = "0123456789ABCDEF";
              let color = "#";
              for (let i = 0; i < 6; i++) {
                  color += letters[Math.floor(Math.random() * 16)];
              }
              return color;
          }
      });
      """

   html = open("index.html", 'w')
   html.write(html_code)
   html.close()

   css = open('styles.css', "w")
   css.write(css_code)
   css.close()

   js = open('script.js', "w")
   js.write(js_code)
   js.close()