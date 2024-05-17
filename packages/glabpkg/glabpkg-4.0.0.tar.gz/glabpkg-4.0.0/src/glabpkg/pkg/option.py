from pathlib import Path

from pkglts.local import pkg_full_name
from pkglts.option.doc.badge import Badge
from pkglts.option_object import Option

from glabpkg.version import __version__


class OptionGlabPkg(Option):
    def version(self):
        return __version__

    def root_dir(self):
        return Path(__file__).parent

    def update_parameters(self, cfg):
        # add a parameter to the option
        return super().update_parameters(cfg)

    def check(self, cfg):
        invalid_params = []

        return invalid_params

    def require_option(self, cfg):
        return ['glabpkg_dev', 'pypi', 'conda']

    def environment_extensions(self, cfg):
        if "/" in cfg['gitlab']['owner']:
            gr = cfg['gitlab']['owner'].split("/")
            group_owner = gr[0]
            subgroup_owner = "/".join(gr[1:]) + "/"
        else:
            group_owner = cfg['gitlab']['owner']
            subgroup_owner = ""

        pages_url = f"https://{group_owner}.gitlab.io/{subgroup_owner}{cfg['gitlab']['project']}/"
        # pip
        ver = cfg['version']
        url = (f"https://pypi.org/project/{cfg['gitlab']['project']}"
               f"/{ver['major']:d}.{ver['minor']:d}.{ver['post']:d}/")
        img = f"{pages_url}_images/badge_pkging_pip.svg"
        badge_pip = Badge(
            name="pip",
            url=url,
            url_img=img,
            text="PyPI version"
        )
        # conda
        url = f"https://anaconda.org/revesansparole/{pkg_full_name(cfg)}"
        img = f"{pages_url}_images/badge_pkging_conda.svg"
        badge_conda = Badge(
            name="conda",
            url=url,
            url_img=img,
            text="Conda version"
        )

        return {"badges": [badge_pip, badge_conda]}
