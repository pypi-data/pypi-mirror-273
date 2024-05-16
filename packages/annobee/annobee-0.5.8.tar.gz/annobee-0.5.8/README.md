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
        <pre><code>git clone https://github.com/variantAnnotation/annobee-sdk </code></pre>
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

<h4> </4>

<h4>Example 1: Evaluate Specific Criteria (PS1)</h4>
<pre><code>annobee 1-14973-A-AG -ps1</code></pre>
<p> It returns : </p>
<pre><code>  { "PS1": 0 }</code></pre>

<h4>Example 2: Evaluate Specific Criterias more then One (PS1, BP7, PP2 etc)</h4>
<pre><code>annobee 1-14973-A-AG -ps1</code></pre>
<p> It returns : </p>
<pre><code>   {
    "PS1": 0,
    "BP7": 1,
    "PP2": 0,
    "BS1": 0,
    "PP5": 0
} </code></pre>

<h4>Example 3: Evaluate All Criteria and pathogenicity</h4>
<pre><code>annobee 1-14973-A-AG -all</code></pre>
<p> It returns : </p>
<pre><code>
    {"PS1": 0,
    "PM5": 0,
    "BP7": 1,
    "PVS1": 1,
    "BP1": 0,
    "PP2": 0,
    "PS4": 0,
    "BS1": 0,
    "BS2": 1,
    "PM2": 0,
    "PM1": 0,
    "PP5": 0,
    "BP6": 0,
    "BA1": 1,
    "PP3": 0,
    "BP4": 1,
    "PM4": 1,
    "BP3": 0,
    "VA_PATHOGENICITY": "Pathogenic"}
</code></pre>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<h2>Usage as python library</h2>

Here's a simple script that evaluates multiple variants using the `annobee` SDK:

```python
import json
from annobee import Annobee

def evaluate_variant(annobee, variant, criteria):
    variant_info = annobee.get_criteria(variant)
    results = {}
    
    if criteria == 'all':
        results = annobee.get_all(variant_info)
    else:
        for criterion in criteria:
            if criterion == 'PS1':
                results['PS1'] = annobee.get_ps1(variant_info)
            elif criterion == 'PM5':
                results['PM5'] = annobee.get_pm5(variant_info)
            elif criterion == 'BP7':
                results['BP7'] = annobee.get_bp7(variant_info)
            elif criterion == 'PVS1':
                results['PVS1'] = annobee.get_pvs1(variant_info)
            # Add more criteria as needed
            
    return results

if __name__ == '__main__':
    # Set the endpoint
    endpoint = 'http://localhost:5000/api/interpret'
    annobee = Annobee(endpoint=endpoint)

    # List of variants
    variants = [
        '1-14973-A-AG',
        '2-23214-G-T',
        '3-45321-C-A',
        '4-55423-T-G',
        '5-67432-A-C'
    ]

    # Evaluate one criterion for one variant
    print("Evaluating one criterion (PS1) for one variant:")
    result_one_criterion = evaluate_variant(annobee, variants[0], ['PS1'])
    print(json.dumps(result_one_criterion, indent=4))

    # Evaluate three criteria for one variant
    print("\nEvaluating three criteria (PS1, PM5, BP7) for one variant:")
    result_three_criteria = evaluate_variant(annobee, variants[0], ['PS1', 'PM5', 'BP7'])
    print(json.dumps(result_three_criteria, indent=4))

    # Evaluate all criteria for one variant
    print("\nEvaluating all criteria for one variant:")
    result_all_criteria = evaluate_variant(annobee, variants[0], 'all')
    print(json.dumps(result_all_criteria, indent=4))
```



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
