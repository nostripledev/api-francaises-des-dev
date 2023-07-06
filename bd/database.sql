--
-- Base de données : `API_francaises_des_dev`
--

-- --------------------------------------------------------

--
-- Structure de la table `category`
--

CREATE TABLE `category` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `member`
--

CREATE TABLE `member` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `lastname` varchar(50) NOT NULL,
  `firstname` varchar(50) NOT NULL,
  `description` text NOT NULL,
  `mail` varchar(320) NOT NULL,
  `date_validate` datetime DEFAULT NULL,
  `date_deleted` datetime DEFAULT NULL,
  `url_portfolio` varchar(320) NOT NULL,
  `image_portfolio` longblob NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `member_has_category`
--

CREATE TABLE `member_has_category` (
  `id_member` int(11) NOT NULL,
  `id_category` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `member_has_network`
--

CREATE TABLE `member_has_network` (
  `id_member` int(11) NOT NULL,
  `id_network` int(11) NOT NULL,
  `url` varchar(355) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `network`
--

CREATE TABLE `network` (
  `Id` int(11) NOT NULL,
  `name` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `category`
--
ALTER TABLE `category`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `member`
--
ALTER TABLE `member`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `member_has_category`
--
ALTER TABLE `member_has_category`
  ADD KEY `id_member` (`id_member`),
  ADD KEY `id_category` (`id_category`);

--
-- Index pour la table `member_has_network`
--
ALTER TABLE `member_has_network`
  ADD UNIQUE KEY `unique_member_network` (`id_member`,`id_network`),
  ADD KEY `id_member` (`id_member`),
  ADD KEY `id_network` (`id_network`);

--
-- Index pour la table `network`
--
ALTER TABLE `network`
  ADD PRIMARY KEY (`Id`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `category`
--
ALTER TABLE `category`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `member`
--
ALTER TABLE `member`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `network`
--
ALTER TABLE `network`
  MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `member_has_category`
--
ALTER TABLE `member_has_category`
  ADD CONSTRAINT `member_has_category_ibfk_1` FOREIGN KEY (`id_member`) REFERENCES `member` (`id`),
  ADD CONSTRAINT `member_has_category_ibfk_2` FOREIGN KEY (`id_category`) REFERENCES `category` (`id`);

--
-- Contraintes pour la table `member_has_network`
--
ALTER TABLE `member_has_network`
  ADD CONSTRAINT `member_has_network_ibfk_1` FOREIGN KEY (`id_member`) REFERENCES `member` (`id`),
  ADD CONSTRAINT `member_has_network_ibfk_2` FOREIGN KEY (`id_network`) REFERENCES `network` (`Id`);
COMMIT;
