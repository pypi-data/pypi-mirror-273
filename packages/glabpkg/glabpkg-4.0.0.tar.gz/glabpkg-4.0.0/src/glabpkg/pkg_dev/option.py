from pathlib import Path

from pkglts.option.doc.badge import Badge
from pkglts.option_object import Option

from glabpkg.version import __version__


class OptionGlabPkgDev(Option):
    def version(self):
        return __version__

    def root_dir(self):
        return Path(__file__).parent

    def update_parameters(self, cfg):
        cfg['base']['authors'] = [('revesansparole', 'revesansparole@gmail.com')]

        for ext in [".csv", ".ini", ".json", ".rst", ".svg"]:
            if ext not in cfg['data']['filetype']:
                cfg['data']['filetype'].append(ext)
        cfg['data']['use_ext_dir'] = False

        cfg['doc']['fmt'] = "rst"

        cfg['pyproject']['intended_versions'] = ["3.10", "3.11"]

        cfg['sphinx']['theme'] = "sphinx_rtd_theme"
        cfg['sphinx']['gallery'] = "example"

        cfg['test']['suite_name'] = "pytest"

        cfg['gitlab']['server'] = "gitlab.com"

        # add a parameter to the option
        return super().update_parameters(cfg)

    def check(self, cfg):
        invalid_params = []

        return invalid_params

    def require_option(self, cfg):
        return ['glabbase', 'pyproject', 'sphinx', 'coverage', 'data']

    def environment_extensions(self, cfg):
        if "/" in cfg['gitlab']['owner']:
            gr = cfg['gitlab']['owner'].split("/")
            group_owner = gr[0]
            subgroup_owner = "/".join(gr[1:]) + "/"
        else:
            group_owner = cfg['gitlab']['owner']
            subgroup_owner = ""

        url = f"https://{group_owner}.gitlab.io/{subgroup_owner}{cfg['gitlab']['project']}/"
        img = f"{url}_images/badge_doc.svg"
        badge = Badge(
            name="doc",
            url=url,
            url_img=img,
            text="Documentation status"
        )

        return {"badges": [badge]}
