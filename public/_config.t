environment production;
basepath /;
baseurl https://192.168.30.128;
title Test;
description Test Taiga site;
disallow_sysfiles true;
allowed_sysfiles _css;
footer_year <<!---->? echo date("Y")?>;
footer_text <a href="https://github.com/ProjectCros/cros">Proudly powered by cros.</a>;
