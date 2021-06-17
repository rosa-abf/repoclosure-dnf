FROM rosalab/rosa2019.1

RUN dnf --nogpgcheck --refresh --assumeyes --nodocs --setopt=install_weak_deps=False upgrade \
 && rm -f /etc/localtime \
 && ln -s /usr/share/zoneinfo/UTC /etc/localtime \
 && dnf --nogpgcheck --assumeyes --nodocs --setopt=install_weak_deps=False install dnf-utils rosa-repos \
 && dnf --nogpgcheck --assumeyes --nodocs --setopt=install_weak_deps=False install make python3-cheetah \
 && dnf autoremove --assumeyes \
 && dnf clean all \
 && rm -rf /var/cache/dnf/* \
 && rm -rf /var/lib/dnf/yumdb/* \
 && rm -rf /var/lib/dnf/history/* \
 && rm -rf /tmp/* \
 && rm -rf /var/lib/rpm/__db.* \
 && rm -rf /usr/share/man/ /usr/share/cracklib /usr/share/doc

WORKDIR /repoclosure
COPY repoclosure.py ./
COPY Makefile ./
COPY repoclosure ./repoclosure
RUN make
ENTRYPOINT ["/repoclosure/repoclosure.py"]
