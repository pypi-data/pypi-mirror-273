<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->


<!-- ABOUT THE PROJECT -->
<h2>About The Project</h2>

<p>
    <code>annobee-sdk</code> is designed to analyze genetic variants to determine their pathogenicity using multiple established criteria. It integrates several functions to set various genetic criteria based on evolutionary conservation, allele frequency, and ACMG/AMP standards. The main functionality is centralized in the <code>main.py</code>.
</p>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<h3>Built With</h3>

<ul>
    <li><a href="https://www.python.org/">Python</a></li>
</ul>

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- GETTING STARTED -->
<h2>Getting Started</h2>

<p>To get a local copy up and running follow these simple example steps.</p>

<h3>Prerequisites</h3>

<ul>
    <li>Python: Download Python <a href="https://www.python.org/downloads/">here</a>.</li>
</ul>

<h3>Requirements</h3>

<ul>
    <li>flask==2.0.1</li>
    <li>numpy==1.23.5</li>
    <li>pandas==1.5.3</li>
    <li>requests==2.25.1</li>
    <li>tqdm==4.65.0</li>
</ul>

<h3>Installation</h3>

<ol>
    <li>Clone the repo
        <pre><code>git clone https://github.com/yourusername/annobee-sdk.git</code></pre>
    </li>
    <li>Follow to directory where you clone the repo:
        <pre><code>cd annobee-sdk</code></pre>
    </li>
    <li>Install requirements and dependencies:
        <pre><code>pip install -r requirements.txt</code></pre>
    </li>
</ol>

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
<h2>Usage</h2>

<h3> Downloading annobee</h3>
<pre><code>pip install annobee</code></pre>

<h3>Command-Line Interface</h3>

<p>To use the <code>annobee-sdk</code>, you can execute the CLI tool with various options to evaluate genetic variant criteria.</p>

<h4>Example 1: Evaluate Specific Criteria (PS1)</h4>
<pre><code>annobee 1-14973-A-AG -ps1</code></pre>

<h4>Example 2: Evaluate All Criteria</h4>
<pre><code>annobee 1-14973-A-AG -all</code></pre>

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
<h2>Roadmap</h2>

<ul>
    <li>[ ] Adding testing metrics regarding the performance of the platform</li>
</ul>

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
<h2>Contributing</h2>

<p>Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are <strong>greatly appreciated</strong>.</p>

<p>If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement". Don't forget to give the project a star! Thanks again!</p>

<ol>
    <li>Fork the Project</li>
    <li>Create your Feature Branch (<code>git checkout -b feature/AmazingFeature</code>)</li>
    <li>Commit your Changes (<code>git commit -m 'Add some AmazingFeature'</code>)</li>
    <li>Push to the Branch (<code>git push origin feature/AmazingFeature</code>)</li>
    <li>Open a Pull Request</li>
</ol>

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
<h2>License</h2>

<p>Distributed under the MIT License. See <code>LICENSE.txt</code> for more information.</p>

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
<a href="https://www.python.org/">Python</a>
