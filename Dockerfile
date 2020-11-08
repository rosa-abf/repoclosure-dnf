FROM rosalab/rosa2019.1

RUN dnf --nogpgcheck --refresh --assumeyes --nodocs --setopt=install_weak_deps=False upgrade \
 && rm -f /etc/localtime \
 && ln -s /usr/share/zoneinfo/UTC /etc/localtime \
 && dnf --nogpgcheck --assumeyes --nodocs --setopt=install_weak_deps=False install dnf-utils rosa-repos \
 && dnf autoremove --assumeyes \
 && dnf clean all \
 && rm -rf /var/cache/dnf/* \
 && rm -rf /var/lib/dnf/yumdb/* \
 && rm -rf /var/lib/dnf/history/* \
 && rm -rf /tmp/* \
 && rm -rf /var/lib/rpm/__db.* \
 && rm -rf /usr/share/man/ /usr/share/cracklib /usr/share/doc \
 && dnf install make python3egg\(pip\) \
 && pip3 install cheetah3

WORKDIR /repoclosure
COPY repoclosure.py ./
COPY Makefile ./
COPY repoclosure ./repoclosure
RUN make
ENTRYPOINT ["/repoclosure/repoclosure.py"]