<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Computer Science Report Examination Number 0000000</title>
    <link rel="stylesheet" type="text/css" href="report.css">
    <script src="report.js" defer></script>
</head>

<body>
    <div class="header">
        <div class="header-img">
        </div>
    </div>

    <div id="navcontainer">
        <ul id="navlist">
            <li><a href="index.html" class="active">Home</a></li>
            <li><a href="brhome.html">BR3</a></li>
            <li><a href="graphing.html">AR1</a></li>
            <li><a href="bird_maker.html">AR2 & AR3</a></li>
        </ul>
    </div>

    <section id="main">
        <h1 id="title">Computer Science Project 2025</h1>
        <h1 id="title">Name of Project</h1>
        <h1 id="title">Exam Number: 258530</h1>
        <div id="pheading"></div>

        <div class="fcon">
            <form>
                <center>
                    <label for="name">User Name</label>
                    <input type="text" id="name" name="name" placeholder="TYPE HERE..." required>
                    <br><br>

                    <label for="breed">Breed:</label>
                    <select id="breed" required>
                        <option value="">Select Breed</option>
                        <option value="Mourning dove">Mourning dove</option>
                        <option value="Canada goose">Canada goose</option>
                        <option value="European starling">European starling</option>
                        <option value="Killdeer">Killdeer</option>
                        <option value="Rock pigeon">Rock pigeon</option>
                        <option value="Barn swallow">Barn swallow</option>
                        <option value="Red-tailed hawk">Red-tailed hawk</option>
                        <option value="Ring-billed gull">Ring-billed gull</option>
                        <option value="House sparrow">House sparrow</option>
                        <option value="American kestrel">American kestrel</option>
                    </select>

                    <label for="size">Size:</label>
                    <select id="size" required>
                        <option value="">Select Size</option>
                        <option value="Small">Small</option>
                        <option value="Medium">Medium</option>
                        <option value="Large">Large</option>
                    </select>
                    <br><br>

                    <p>Choose the airlines that you would consider flying with:</p>
                    <input type="checkbox" id="al1" name="al1" value="SOUTHWEST AIRLINES">
                    <label for="al1">Southwest Airlines</label>
                    <input type="checkbox" id="al2" name="al2" value="BUSINESS">
                    <label for="al2">Business</label>
                    <input type="checkbox" id="al3" name="al3" value="AMERICAN AIRLINES">
                    <label for="al3">American Airlines</label>
                    <input type="checkbox" id="al4" name="al4" value="DELTA AIR LINES">
                    <label for="al4">Delta Airlines</label>
                    <input type="checkbox" id="al5" name="al5" value="AMERICAN EAGLE AIRLINES">
                    <label for="al5">American Eagle Airlines</label>
                    <br><br>

                    <label for="cloud">Is the day you are choosing to fly on cloudy?:</label>
                    <select id="cloud" required>
                        <option value="">Select Yes/No</option>
                        <option value="True">Yes</option>
                        <option value="False">No</option>
                    </select>
                    <br>
                    <button type="button" id="sendToFb">Submit Data</button>
                </center>

                <table>
                    <thead>
                        <tr>
                            <th>User Name</th>
                            <th>Breed</th>
                            <th>Size</th>
                            <th>Airlines</th>
                            <th>Clouds</th>
                        </tr>
                    </thead>
                    <tbody id="ar2data"></tbody>
                </table>
                <br>
                <center>\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\</center>
                <br>
            </form>
        </div>
    </section>

    <blockquote>
        <table>
            <thead>
                <tr>
                    <th>User Name</th>
                    <th>Safety Recommendations</th>
                </tr>
            </thead>
            <tbody id="ar3data"></tbody>
        </table>
    </blockquote>

    <script src="https://www.gstatic.com/firebasejs/7.20.0/firebase.js"></script>
    <script src="bird_maker.js" defer></script>

    <section id="footer">
        &copy; 258530
    </section>
</body>
</html>


