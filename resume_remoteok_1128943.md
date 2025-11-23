\documentclass[11pt]{article}
\usepackage[letterpaper, top=0.5in, bottom=0.5in, left=0.5in, right=0.5in]{geometry}

\usepackage[utf8]{inputenc}
\usepackage{enumitem}
\usepackage[hidelinks]{hyperref}
\usepackage{titlesec}
\raggedright
\pagestyle{empty}
\input{glyphtounicode}
\pdfgentounicode=1

\titleformat{\section}{\bfseries\large}{}{0pt}{}[\vspace{1pt}\titlerule\vspace{-6.5pt}]
\renewcommand\labelitemi{$\vcenter{\hbox{\small$\bullet$}}$}
\setlist[itemize]{itemsep=-2pt, leftmargin=12pt, topsep=7pt}

\begin{document}

\begin{center}
\Huge Jane Doe
\end{center}

\vspace{5pt}

\centerline{\href{mailto:jane.doe@gmail.com}{jane.doe@gmail.com} | \href{https://github.com/jane-doe}{github.com/jane-doe} | \href{https://www.linkedin.com/in/jane-doe}{linkedin.com/in/jane-doe}}

\vspace{-10pt}

\section*{Skills}
\textbf{Programming Languages:} Python, JavaScript, TypeScript \\
\textbf{Frameworks:} React, Node.js, Express \\
\textbf{Cloud Platforms:} AWS, Google Cloud Platform \\
\textbf{DevOps:} Terraform, Docker, Kubernetes \\
\textbf{Databases:} SQL, MongoDB \\
\textbf{Other:} Git, Agile, Scrum

\vspace{-6.5pt}

\section*{Achievements}
\textbf{Led migration to AWS with Infrastructure as Code:} Moved legacy services to AWS using Terraform, reducing infrastructure costs by 30\%.
\begin{itemize}
    \item Action: Migrated legacy services to AWS
    \item Context: Implemented Infrastructure as Code with Terraform
    \item Result: Reduced infrastructure costs by 30\%
\end{itemize}

\textbf{Developed and maintained a high-traffic web application:} Built and maintained a React-based web application using Node.js and Express, ensuring high availability and performance.
\begin{itemize}
    \item Action: Developed and maintained a high-traffic web application
    \item Context: Utilized React, Node.js, and Express
    \item Result: Ensured high availability and performance
\end{itemize}

\textbf{Optimized database queries for improved performance:} Identified and optimized slow-running SQL queries, reducing query execution time by 50\%.
\begin{itemize}
    \item Action: Identified and optimized slow-running SQL queries
    \item Context: Analyzed database performance using SQL profiling tools
    \item Result: Reduced query execution time by 50\%
\end{itemize}

\textbf{Implemented CI/CD pipeline for automated deployments:} Set up a CI/CD pipeline using Jenkins and Docker, enabling automated deployments and reducing deployment time by 75\%.
\begin{itemize}
    \item Action: Set up a CI/CD pipeline
    \item Context: Utilized Jenkins, Docker, and Kubernetes
    \item Result: Reduced deployment time by 75\%
\end{itemize}

\textbf{Collaborated with cross-functional teams to deliver projects on time:} Worked closely with product managers, designers, and other developers to deliver projects on time and within budget.
\begin{itemize}
    \item Action: Collaborated with cross-functional teams
    \item Context: Communicated effectively and managed project timelines
    \item Result: Delivered projects on time and within budget
\end{itemize}

\vspace{-18.5pt}

\section*{Projects}
\textbf{Project Title: High-Traffic Web Application} \hfill \href{https://github.com/jane-doe/high-traffic-web-app}{github.com/jane-doe/high-traffic-web-app}
\begin{itemize}
    \item Developed a high-traffic web application using React, Node.js, and Express
    \item Implemented Infrastructure as Code with Terraform for AWS deployment
    \item Optimized database queries for improved performance
\end{itemize}

\textbf{Project Title: CI/CD Pipeline} \hfill \href{https://github.com/jane-doe/ci-cd-pipeline}{github.com/jane-doe/ci-cd-pipeline}
\begin{itemize}
    \item Set up a CI/CD pipeline using Jenkins and Docker
    \item Automated deployments and reduced deployment time by 75\%
    \item Implemented Kubernetes for container orchestration
\end{itemize}

\vspace{-18.5pt}

\section*{Education}
\textbf{School} -- PhD in Computer Science \hfill June 2015 \\
\textbf{School} -- MS in Computer Science \hfill June 2012 \\
\textbf{School} -- BS in Computer Science \hfill Apr 2009

\vspace{-18.5pt}

\section*{Certifications}
\textbf{Certification Name} -- Issuer \hfill Date
\href{https://certificate-link.com}{Certificate Link},

\end{document}