# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Gm2pip(Package):
    """Wrapper for python packages for gm2"""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/gm2"
    url = "https://cdcvs.fnal.gov/redmine/projects/gm2"

    maintainers = ["marcmengel"]

    version("1.1.0")

    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-pyinotify", type=("build", "run"))
    depends_on("py-python-dateutil", type=("build", "run"))
    depends_on("py-pandas", type=("build", "run"))
    depends_on("py-ipython", type=("build", "run"))
    depends_on("py-ipykernel", type=("build", "run"))
    depends_on("py-widgetsnbextension", type=("build", "run"))
    depends_on("py-ipywidgets", type=("build", "run"))
    depends_on("py-ipywe", type=("build", "run"))
    depends_on("py-jupyter", type=("build", "run"))
    depends_on("py-jupyterlab", type=("build", "run"))
    depends_on("py-jupyterlab-server", type=("build", "run"))
    depends_on("py-jupyterlab-launcher", type=("build", "run"))
    depends_on("py-jupyterlab-widgets", type=("build", "run"))
    depends_on("py-jupyterlab-templates", type=("build", "run"))
    depends_on("py-plotly", type=("build", "run"))
    depends_on("py-jupyter-full-width", type=("build", "run"))  # ?
    depends_on("py-jltheme", type=("build", "run"))  # ?
    depends_on("py-plotly-scientific-plots", type=("build", "run"))  # ?
    depends_on("py-rplotmaker", type=("build", "run"))  # ?
    depends_on("py-matplotlylib", type=("build", "run"))  # ?
    depends_on("py-julia", type=("build", "run"))  # ?

    # packages now commented out in old requirements file:
    #   IPython-Dashboard
    #   ipython-animated-array
    #   ipyext
    #   r2_kernel - An R wrapper kernel for IPython
    #   restmagic - HTTP REST magic for IPython
    #   notedown - Convert markdown to IPython notebook.
    #   ipnb - IPython Notebook code reuse
    #   ipython_genutils - Vestigial utilities from IPython
    #   ipyviz (1.0) - Visualisation package for IPython Notebooks
    #   itable (0.0.1) - View pretty tables in IPython
    #   jupyter-js-widgets-nbextension (0.0.2.dev0)  - IPython HTML widgets for Jupyter
    #   jython-kernel (2.0) - A Jython kernel for Jupyter/IPython
    #   mdma (0.1.6) - ipython notebook markdown magic
    #   fileupload (0.1.5) - IPython file upload widget
    #   calysto (1.0.6) - Libraries and Languages for Python and IPython
    #   colorlover (0.2.1) - Color scales for IPython notebook
    #   failed to install: hdf5widget #(0.1.0)
    #   - This is hdf5widget, a widget for viewing the contents of a HDF5-file
    #     in Jupyter Notebooks using ipywidgets.
    #   ipython-memory-usage
    #   ipython-cluster-helper
    #   ipcluster_tools
    #   ptime - IPython magic for parallel profiling
    #   ipyparallel - Interactive Parallel Computing with IPython
    #   jupyter-spy (1.0.0) - Log Jupyter messages
    #   jupyter-ctrl (0.3) - Jupyter Notebooks Controller Daemon
    #   jupyter-sql (0.1.0) - Simple SQL kernel for Jupyter
    #   jupyter-themer (0.4.0) - Custom CSS themer for jupyter notebooks
    #   jupyter-hdfscontents (0.2) - Jupyter content manager that uses the HDFS filesystem
    #   jupyter-parser (0.0a2) - a command line tool for parsing jupyter notebooks
    #   jupyter-progressbar (0.1.6)
    #   - Wrap a generator or iterator with a progress bar in Jupyter Notebooks.
    #   jupyter-tools (0.1.0) - Some tools to make working in jupyter notebooks easier
    #   jupyter-wysiwyg (0.1.8) - WYSIWYG editing functionality for markdown/HTML cells in Jupyter
    #   jupyter-repo2docker (0.6.0)
    #   - Repo2docker: Turn code repositories into Jupyter enabled Docker Images
    #   nbindex-jupyter (0.2.25)
    #   - Javascript based Jupyter Notebook additions (Table of Content, hide code,
    #     Figure numbers, ...)
    #   jupyter-conf-search (0.4.4)
    #   - Utility for searching through jupyter configuration files, using
    #     jupyter's path definitions to find their locations dynamically.
    #   failed to install: jupyter-plotly-dash #(0.0.11)
    #   - Interactive Jupyter use of plotly dash apps
    #   jupyter-docx-bundler (0.1.3) - Jupyter bundler extension to export notebook as a docx file
    #   jupyter-js-widgets-nbextension (0.0.2.dev0)  - IPython HTML widgets for Jupyter
    #   jupyter-cjk-xelatex (0.2)
    #   - Handle the encoding error for jupyter nbconvert to convert notebook to pdf document
    #   indico-plugin-previewer-jupyter (1.0)
    #   - Jupyter notebook rendering for attachments in Indico
    #   jupyter-config (0.7.0) -
    #   qtconsole (4.4.2) - Jupyter Qt console
    #   nbrmd (0.6.0) - Jupyter notebooks as markdown documents, Python or R scripts
    #   jupyterlab-server #(0.2.0) - JupyterLab Server
    #   jupyterlab-latex #(0.4.1)
    #   - A Jupyter Notebook server extension which acts as an endpoint for LaTeX.
    #   plotly-unbrand (1.0.1) - A small package to remove the branding from plotly plots
    #   bashplotlib (0.6.5) - plotting in the terminal
    #   terminalplot (0.2.6) - Plot points in terminal
    #   asciiplotlib (0.1.4) - Plotting on the command line
    #   hpcplot (0.1) - A matplotlib wrapper for HPC Plots
    #   python-node (0.0.4) - A node.js script runner for python
    #   cooperate (0.3.1) - Distribute commands to many nodes
    #   zeroless-tools (0.2.2) - CLI Tools for ZeroMQ™
    #   pyzmp (0.0.17) - ZeroMq based multiprocessing framework.

    def install(self, spec, prefix):
        # packages have to install *something*, so a README...
        f = open(prefix + "README.gm2pip", "w")
        f.write("gm2pip -- wrapper product for gm2 python dependencies\n")
        f.close()
