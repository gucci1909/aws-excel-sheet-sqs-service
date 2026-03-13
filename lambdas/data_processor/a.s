\documentclass[10pt, letterpaper]{article}

% Packages:
\usepackage[
ignoreheadfoot,
top=1cm,
bottom=1cm,
left=1cm,
right=1cm,
footskip=1cm
]{geometry}
\usepackage{titlesec, tabularx, array, xcolor, enumitem, fontawesome5, lastpage, changepage, paracol}
\definecolor{primaryColor}{RGB}{0, 79, 144}
\usepackage[unicode, draft=false]{hyperref}
\color[HTML]{110223}%{1C033C}

% Formatting settings
% \pagestyle{empty}
\setlength{\parindent}{0pt}
\setlength{\columnsep}{0cm}
\titleformat{\section}{\bfseries\large}{}{0pt}{}[\vspace{1pt}\titlerule]
% \titlespacing{\section}{-1pt}{0.3cm}{0.2cm}

\hypersetup{
    colorlinks=true,
    urlcolor=blue,
    hyperfootnotes=false
}

% Packages
\usepackage{xcolor, tcolorbox, titlesec, tabularx, array, enumitem, fontawesome5, hyperref, lastpage, changepage}
\usepackage{geometry}
\geometry{ignoreheadfoot, top=1cm, bottom=1cm, left=1cm, right=1cm, footskip=1cm}

% Define Colors
\definecolor{primaryColor}{RGB}{0, 79, 144} 
\definecolor{textcolor}{RGB}{44, 62, 80}

% Formatting settings
\setlength{\parindent}{0pt}
\setlength{\columnsep}{0cm}
\titleformat{\section}{\large\bfseries\color{primaryColor}}{}{0pt}{}[\vspace{1pt}\titlerule]
\titlespacing{\section}{0pt}{8pt}{4pt}

\begin{document}
\newcommand{\faLeetcode}{\includegraphics[height=0.8em]{leetcode.png}}
\newcommand{\faGfg}{\includegraphics[height=1em]{gfg.png}}


\begin{center}
    % \begin{tcolorbox}[colframe=primaryColor, colback=white, arc=8pt, boxrule=1mm, width=0.8\textwidth]
        {\Huge\bfseries\textcolor{textcolor}{SHAILJA JOSHI}} \\
    % \end{tcolorbox}
    \vspace{0.3cm}
    
    {\quad 
    \faPhone +91-8800480501 \quad \faEnvelope \hspace{1pt} \href{mailto:shailjajoshi13@gmail.com}{shailjajoshi13@gmail.com}  \quad \faLinkedin \hspace{1pt} \href{https://www.linkedin.com/in/shailja-joshi-data-analyst/}{LinkedIn}} \quad
\end{center}
\section{Experience}
\begin{tabularx}{\textwidth}{X r}
    \textbf{Data Engineering Analyst,} Accenture & \textbf{Oct 2022 - Present} \\
\end{tabularx}
\begin{itemize}[noitemsep, topsep=1pt]


% \item Designed and deployed a scalable, plug-and-play \textbf{User-Management Package} using the \textbf{MERN stack} to manage financial user lifecycles (add, suspend, remove). Integrated across \textbf{12+ financial platforms}, reducing user provisioning time by \textbf{75\%} and ensuring \textbf{KYC compliance} with role-based access control and audit logs.

% \item Modernized core infrastructure by integrating \textbf{Elasticsearch} for real-time search and fraud analytics, and \textbf{RabbitMQ} for async transaction workflows—achieving \textbf{4x faster} reporting, \textbf{35\% higher throughput}, and \textbf{99.95\% uptime} during high-volume financial operations.

% \item Spearheaded end-to-end development of \textbf{2 mission-critical fintech systems} (customer onboarding \& loan servicing), delivering \textbf{80+ high-impact features} that streamlined operations and increased customer retention by \textbf{25\%}, with rapid iterations driven by feedback from \textbf{QA/UAT cycles}.

% \item Contributed to a \textbf{Gen AI-powered document intelligence system}, leveraging \textbf{OpenAI APIs} to parse and query financial PDFs. Reduced manual review time by \textbf{60\%}, accelerating compliance audits and insight extraction for faster loan approvals.



   \item Developed and optimized complex SQL queries in Snowflake , enabling data analysis that
    reduced reporting time by \textbf{30\%} and improved data-driven decision-making across departments.

\item Utilized \textbf{Autosys} to schedule data processing tasks, improving operational efficiency by \textbf{20\%}.   

\item Facilitated secure and efficient file transfers using \textbf{WinSCP} , resulting in a 25\% improvement in
data exchange speed and protocol compliance across teams. 

\item Designed and implemented robust ETL pipelines using \textbf{Informatica PowerCenter} ,
transforming and integrating data from multiple sources to improve data quality by 35\% and
support accurate business intelligence reporting. 

\item Implemented an \textbf{automated file ingestion and publishing workflow}, where files received in \textbf{AWS S3} triggered \textbf{AutoSys} alerts that executed scripts and Snowflake procedures to load data via \textbf{external stages into the ETL layer} and publish it to downstream publish layers.
    
\end{itemize}
\vspace{5pt} 


% \begin{tabularx}{\textwidth}{X r}
%     \textbf{Full Stack Developer,} Masai School & \textbf{Jan 2022 - Dec 2022} \\
% \end{tabularx}

% \begin{itemize}[noitemsep, topsep=1pt]
%     \item Completed a rigorous Full Stack Developer training program, delivering 9 major applications and over 40 supplementary projects utilizing JavaScript, Node.js, React.js, Redux, TypeScript, Express.js and MongoDB to enhance coding proficiency.
% \end{itemize}

\section{Projects}
\textbf{GreenLeaf Commerce Analytics} \small{\href{https://github.com/Shailja-Joshi/snowflake-project}{GitHub Link}} \hfill \textit{Snowflake, SQL, ETL/ELT, Medallion Architecture}  
\begin{itemize}[noitemsep, topsep=1pt]
    \item Designed and implemented an end-to-end \textbf {Snowflake ETL pipeline} using a \textbf {Bronze–Silver–Gold architecture} to support governed analytics.
    \item Implemented \textbf{CSV data ingestion} into Snowflake and applied \textbf{SQL-based transformations} to cleanse, standardize, and validate data in the Silver layer.
    \item Enforced \textbf{data quality checks and business rules}, including null handling, deduplication, and referential integrity validations.
    \item Developed \textbf{Gold-layer analytical views} for daily sales aggregation and customer-product affinity analysis using optimized SQL queries.
\end{itemize}

\vspace{2pt} 
\textbf{Enterprise Data Integration and Transformation Pipeline} \href{https://github.com/Shailja-Joshi/Informatica-Data-Integration-and-Transformation-Project}{GitHub Link} \hfill \textit{Informatica PowerCenter,SQL, Data Transformation}  
\begin{itemize}[noitemsep, topsep=1pt]
    \item Built ETL workflows using \textbf{Informatica PowerCenter} to structure and transform relational data across multiple tables.
    \item Created Informatica mappings leveraging \textbf{Aggregator, Joiner, Rank, and Sequence transformations} to implement required transformation logic.
    \item Executed \textbf{SQL-based table setup and data operations}, including table creation, truncation, column alterations, and data insertion.
    \item Ensured \textbf{data consistency and quality} through validation checks and applied basic performance optimization techniques within the ETL flow.
\end{itemize}
\vspace{2pt} 
\section{Technical Skills}
\textbf{Programming Languages:}  
 C++, Python, SQL (MySQL)
\vspace{2pt}

\textbf{Data Warehousing \& Analytics:}  
Snowflake, Data Warehousing
 \vspace{2pt}  

\textbf{ETL \& Integration Tools:}  
Informatica PowerCenter, ETL
\vspace{2pt}  

\textbf{Scheduling \& File Transfer:}  
AutoSys, WinSCP , Putty
\vspace{2pt}  
% Education
\section{Education}

\begin{tabularx}{\linewidth}{ @{}l r@{} }
\color[HTML]{1C033C} \textbf{B.Tech in Computer Science} & \hfill \color[HTML]{371e77} CGPA: 8.4\\
\color[HTML]{371e77} Graphic Era University,Dehradun & \hfill \color[HTML]{4B28A4} \textit{\textbf{ Aug 2018 - Jun 2022 }} \\
\multicolumn{0}{@{}X@{}}{}
\end{tabularx}

\section{Awards and Certificates}
\begin{tabularx}{\linewidth}{ @{}l r@{} }
\begin{minipage}[t]{\linewidth}
  \begin{itemize}[nosep, after=\strut, leftmargin=2em, itemsep=2pt]
    \item \textbf{\href{https://www.linkedin.com/feed/update/urn:li:activity:7358009149219115008/}{SnowPro Core Certification (by SNOWFLAKE)}}: An industry-recognized certification demonstrating strong command in Snowflake architecture and best practices.) .
    \item The Ultimate MySQL Bootcamp on Udemy.
\end{itemize}
\end{minipage}
\end{tabularx}
\end{document}

